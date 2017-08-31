import importlib
import os
import xml.etree.ElementTree as XML

import jenkins

import config
groups_map = importlib.import_module(config.GROUPS_MAP_MODULE_NAME)
import map_utils


def create_server_connection(url, username, password):
    return jenkins.Jenkins(url, username=username, password=password)


def create_or_update_job(jenkins_connection, job_name, create_func, update_func):
    if jenkins_connection.job_exists(job_name):
        update_func()
        print('job "{}" updated'.format(job_name))

    else:
        create_func()
        print('job "{}" created'.format(job_name))


def delete_job(jenkins_connection, job_name):
    print('deleting "{}" job...'.format(job_name))
    jenkins_connection.delete_job(job_name)


def delete_jobs(jenkins_connection, prefix, exclusions=None):
    jobs = jenkins_connection.get_jobs()
    jobs_to_delete = [job['name'] for job in jobs if job['name'].startswith(prefix)]

    if exclusions is None:
        exclusions = list()

    for job_name in jobs_to_delete:
        if job_name not in exclusions:
            delete_job(jenkins_connection, job_name)


def sync_template_job(jenkins_connection, job_name, job_file_name):
    config_file_path = os.path.join(os.path.dirname(__file__), job_file_name)

    with open(config_file_path) as config_file:
        xml_config = config_file.read()

    create_or_update_job(jenkins_connection, job_name,
                         create_func=lambda: jenkins_connection.create_job(job_name, xml_config),
                         update_func=lambda: jenkins_connection.reconfig_job(job_name, xml_config))


def sync_jobs(jenkins_connection):

    if not jenkins_connection.job_exists(config.TEMPLATE_JOB_NAME):
        raise Exception('template job "{}" does not exist! '
                        'execute "sync_template_job" command first'.format(config.TEMPLATE_JOB_NAME))

    map_utils.validate(groups_map.MAP, groups_map.GROUP_SCENARIOS)

    jenkins_server = jenkins_connection
    jenkins_server.scenario_axis = 'scenario'
    jenkins_server.environment_axis = 'environment'
    jenkins_server.base_group_job_name = config.TEMPLATE_JOB_NAME
    jenkins_server.subjobs_parameter = 'subjobs'

    group_job_names = [config.TEMPLATE_JOB_NAME]
    group_job_names += create_or_update_group_jobs(jenkins_server, groups_map.MAP, groups_map.GROUP_SCENARIOS)

    delete_jobs(jenkins_server, config.GROUP_JOB_NAME_PREFIX, exclusions=group_job_names)


def create_or_update_group_jobs(jenkins_server, groups, group_scenarios):
    processed_jobs = list()

    def build_group_job(group_name, subgroups):

        scenarios = group_scenarios.get(group_name)
        job_name = config.create_group_job_name(group_name)
        subjob_names = None

        if subgroups:
            subjob_names = list()
            for subgroup_name in (subgroups,) if isinstance(subgroups, str) else subgroups.keys():
                subjob_names.append(config.create_group_job_name(subgroup_name))

        create_or_update_group_job(jenkins_server,
                                   job_name,
                                   subjob_names,
                                   scenarios)

        processed_jobs.append(job_name)

        if isinstance(subgroups, str):
            build_group_job(subgroups, None)

    map_utils.walk_branches(groups, build_group_job)

    return processed_jobs


def create_or_update_group_job(jenkins_server, job_name, subjob_names, group_scenarios):

    def update_job():
        if group_scenarios:
            scenarios, environments, combination_filter = get_matrix_info(group_scenarios,
                                                                          jenkins_server.scenario_axis,
                                                                          jenkins_server.environment_axis)
        else:
            scenarios, environments, combination_filter = (None, None, None)

        update_group_job(jenkins_server, job_name, subjob_names, scenarios, environments, combination_filter)

    create_or_update_job(jenkins_server, job_name,
                         lambda: (jenkins_server.copy_job(jenkins_server.base_group_job_name, job_name), update_job()),
                         lambda: update_job())


def get_matrix_info(scenarios, scenario_axis, environment_axis):
    '''Returns e.g. (['scenario1', 'scenario2'],
                     ['env1', 'env2'],
                    'scenario_axis=="scenario1" && (environment_axis=="env1" || environment_axis=="env2") ||
                     scenario_axis=="scenario2" && (environment_axis=="env2")'
                     )
    '''
    all_scenarios = scenarios.keys()
    all_environments = set()
    scenario_combinations = list()

    for scenario, environment in scenarios.iteritems():

        environments = (environment,) if isinstance(environment, str) else environment

        for env in environments:
            all_environments.add(env)

        environment_filter = ' || '.join(['{}=="{}"'.format(environment_axis, env) for env in environments])

        scenario_combinations.append('{}=="{}" && ({})'.format(scenario_axis, scenario, environment_filter))

    combination_filter = ' || '.join(scenario_combinations)

    return all_scenarios, all_environments, combination_filter


def update_group_job(jenkins_server, job_name, subjob_names, scenarios, environments, combination_filter):

    xml_root = XML.fromstring(jenkins_server.get_job_config(jenkins_server.base_group_job_name))

    xml_root.find('description').text = 'This this auto generated group job.\n' \
                                        'Do not edit! All changes will be lost during synchronization!'

    for projects_elem in xml_root.findall('*//projects'):

        if projects_elem.text == 'scenario_job':
            projects_elem.text = config.SCENARIO_JOB_NAME

        elif projects_elem.text == 'subjobs_list':
            projects_elem.text = ', '.join(subjob_names) if subjob_names else None

    for arg1_elem in xml_root.findall('*//arg1'):
        if arg1_elem.text == 'subjobs_list':
            arg1_elem.text = ', '.join(subjob_names) if subjob_names else None
            break

    if scenarios is None or environments is None:
        xml_root.find('properties').clear()

    if scenarios:
        scenarios_item = xml_root.find('./axes//*[name="{}"]/values'.format(jenkins_server.scenario_axis))
        scenarios_item.clear()
        for scenario in scenarios:
            XML.SubElement(scenarios_item, 'string').text = scenario

    if environments:
        testbeds_item = xml_root.find('./axes//*[name="{}"]/values'.format(jenkins_server.environment_axis))
        testbeds_item.clear()
        for environment in environments:
            XML.SubElement(testbeds_item, 'string').text = environment

    if combination_filter:
        combinationFilter = xml_root.find('combinationFilter')

        if combinationFilter is None:
            combinationFilter = XML.SubElement(xml_root, 'combinationFilter')

        combinationFilter.text = combination_filter

    jenkins_server.reconfig_job(job_name, XML.tostring(xml_root))
    jenkins_server.enable_job(job_name)

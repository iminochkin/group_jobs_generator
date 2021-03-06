import argparse

import config
import jenkins_utils

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name', help='sub-command help')

    subparsers.add_parser('sync_template_jobs',
                          help='creates or updates template job used for generation other jenkins jobs')

    subparsers.add_parser('sync_jobs',
                          help='creates new, updates existent and deletes redundant '
                               'autogenerated jenkins jobs')

    subparsers.add_parser('delete_template_jobs', help='deletes template job used for generation other jenkins jobs')
    subparsers.add_parser('delete_jobs', help='deletes autogenerated jenkins jobs')

    arguments = parser.parse_args()

    jenkins_connection = jenkins_utils.create_server_connection(config.JENKINS_URL,
                                                                config.JENKINS_USER, config.JENKINS_PASSWORD)

    if arguments.subparser_name == 'sync_template_jobs':
        jenkins_utils.sync_template_job(jenkins_connection, config.TEMPLATE_JOB_NAME, config.TEMPLATE_JOB_FILE_NAME)

        if config.SCENARIO_JOB_NAME == config.DEFAULT_SCENARIO_JOB_NAME:
            jenkins_utils.sync_template_job(jenkins_connection,
                                            config.DEFAULT_SCENARIO_JOB_NAME,
                                            config.DEFAULT_SCENARIO_JOB_FILE_NAME)

    elif arguments.subparser_name == 'sync_jobs':
        jenkins_utils.sync_jobs(jenkins_connection)

    elif arguments.subparser_name == 'delete_template_jobs':
        jenkins_utils.delete_job(jenkins_connection, config.TEMPLATE_JOB_NAME)

        if config.SCENARIO_JOB_NAME == config.DEFAULT_SCENARIO_JOB_NAME:
            jenkins_utils.delete_job(jenkins_connection, config.DEFAULT_SCENARIO_JOB_NAME)

    elif arguments.subparser_name == 'delete_jobs':
        jenkins_utils.delete_jobs(jenkins_connection, config.GROUP_JOB_NAME_PREFIX,
                                  exclusions=[config.TEMPLATE_JOB_NAME])

    else:
        raise Exception('undefined command "{}" called'.format(arguments.subparser_name))

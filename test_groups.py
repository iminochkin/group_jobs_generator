# Test scenarios

agent_bvt = 'Agent_BVT'
agent_cbt_fbvt = 'Agent_CBT'
agent_smoke = 'Agent_Smoke'
backup_recovery_basic_fat = 'Backup_Recovery_Basic_FAT'
cmd_wa = 'CMD_WA'
esx_backup_recovery_basic_fbvt = 'ESX_Backup_Recovery_Basic'
esx_vmotion_migrate_backup_fbvt = 'ESX_vMotion_Migrate_and_Backup'
file_recovery_into_vm_fbvt = 'File_Recovery_Into_VM'
finalize_vm_agent_fbvt = 'Finalize_VM_Agent'
hv_backup_recovery_basic_fbvt = 'HV_Backup_Recovery_Basic'
hv_backup_recovery_gen1_bios_fbvt = 'HV_Backup_Recovery_Gen1_BIOS'
hv_backup_recovery_gen2_bios_uefi_fbvt = 'P1_HV_Backup_Recovery_Gen2_BIOS_UEFI'
hv_backup_recovery_on_smb_30_fbvt = 'HV_Backup_Recovery_on_SMB_3.0'
incremental_restore_fbvt = 'Incremental_Restore'
non_quiesced_snapshot_backup_fbvt = 'Non_Quiesced_Snapshot_Backup'
pcs_basic_checks_vms_fbvt = 'PCS_Basic_Checks_VMs'
pcs_basic_checks_cts_fbvt = 'PCS_Basic_Checks_CTs'
run_vm_from_backup_fbvt = 'Run_VM_From_Backup'
vm_replication_fbvt = 'VM_Replication'
vm_snapshot_creation_retry_options_fbvt = 'VM_Snapshot_Creation_Retry_Options'
working_with_hypervisor_agent_fbvt = 'Working_With_Hypervisor_Agent'

# Test environments

esx_55_managed_wa_win_cmd = 'esx_55_managed_wa_win_cmd'
esx_55_managed_wa_rest = 'esx_55_managed_wa_rest'
esx_55_managed_va_win_cmd = 'esx_55_managed_va_win_cmd'
esx_55_managed_va_rest = 'esx_55_managed_va_rest'
esx_55_standalone_wa_win_cmd = 'esx_55_standalone_wa_win_cmd'
esx_55_standalone_wa_lin_cmd = 'esx_55_standalone_wa_lin_cmd'
esx_55_standalone_wa_rest = 'esx_55_standalone_wa_rest'
esx_55_standalone_wa_msp = 'esx_55_standalone_wa_msp'
esx_55_standalone_va_win_cmd = 'esx_55_standalone_va_win_cmd'
esx_55_standalone_va_rest = 'esx_55_standalone_va_rest'
hv_8_win_cmd = 'hv_8_win_cmd'
hv_12_win_cmd = 'hv_12_win_cmd'
hv_12_rest = 'hv_12_rest'
hv_12_msp = 'hv_12_msp'
pcs_rest = 'pcs_rest'
pcs_rest_small = 'pcs_rest_small'
pcs_msp_small = 'pcs_msp_small'
pcs_win_cmd = 'pcs_win_cmd'
pcs_win_cmd_vm = 'pcs_win_cmd_vm'
pcs_win_cmd_ct = 'pcs_win_cmd_ct'

# Smoke tests
Smoke_1_tests = {
    agent_smoke: (hv_12_rest, pcs_rest_small, esx_55_standalone_va_rest, esx_55_standalone_wa_rest),
}

Smoke_2_tests = {
    agent_smoke: (hv_12_msp, pcs_msp_small, esx_55_standalone_wa_msp),
}

# P1 tests
P1_tests = {
    agent_cbt_fbvt: (hv_12_rest, pcs_win_cmd_vm, pcs_win_cmd_ct, esx_55_managed_wa_win_cmd, esx_55_managed_va_win_cmd),
    file_recovery_into_vm_fbvt: (esx_55_managed_wa_win_cmd, esx_55_managed_va_win_cmd),
    finalize_vm_agent_fbvt: esx_55_managed_wa_win_cmd,
    incremental_restore_fbvt: (hv_12_win_cmd, esx_55_managed_wa_win_cmd),
    pcs_basic_checks_cts_fbvt: pcs_win_cmd,
    pcs_basic_checks_vms_fbvt: pcs_win_cmd,
    vm_replication_fbvt: esx_55_standalone_wa_rest,
    working_with_hypervisor_agent_fbvt: (hv_12_rest, esx_55_managed_wa_rest, esx_55_managed_va_rest),
}

# P2 tests
P2_tests = {
    agent_bvt: (hv_8_win_cmd, hv_12_win_cmd, esx_55_managed_wa_win_cmd, esx_55_managed_va_win_cmd),
    esx_backup_recovery_basic_fbvt: (esx_55_managed_wa_win_cmd, esx_55_managed_va_win_cmd),
    vm_replication_fbvt: (esx_55_standalone_wa_win_cmd, esx_55_standalone_va_win_cmd),
    run_vm_from_backup_fbvt: (hv_12_win_cmd, esx_55_managed_wa_win_cmd, esx_55_managed_va_win_cmd),
    hv_backup_recovery_basic_fbvt: hv_12_win_cmd,
}

# P3 tests
P3_tests = {
    cmd_wa: (esx_55_standalone_wa_lin_cmd, esx_55_standalone_wa_win_cmd),
    hv_backup_recovery_gen1_bios_fbvt: hv_8_win_cmd,
    hv_backup_recovery_on_smb_30_fbvt: hv_12_win_cmd,
    non_quiesced_snapshot_backup_fbvt: (esx_55_managed_wa_rest, esx_55_managed_va_rest, pcs_rest),
    hv_backup_recovery_gen2_bios_uefi_fbvt: hv_12_win_cmd,
    vm_snapshot_creation_retry_options_fbvt: (esx_55_managed_wa_rest, esx_55_managed_va_rest),
    esx_vmotion_migrate_backup_fbvt: (esx_55_managed_wa_rest, esx_55_managed_va_rest),
    backup_recovery_basic_fat: hv_12_win_cmd,
}

Smoke_1 = 'Smoke_1'
Smoke_2 = 'Smoke_2'
P1_default = 'P1_default'
P2_default = 'P2_default'
P3_default = 'P3_default'

MAP = {'All':
            {"Smoke": {Smoke_1: None, Smoke_2: None},
             "P1": P1_default,
             "P2": P2_default,
             "P3": P3_default
            }
      }

GROUP_SCENARIOS = {Smoke_1: Smoke_1_tests,
                   Smoke_2: Smoke_2_tests,
                   P1_default: P1_tests,
                   P2_default: P2_tests,
                   P3_default: P3_tests,
                   }

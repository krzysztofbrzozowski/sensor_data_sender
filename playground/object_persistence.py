import shelve

if __name__ == '__main__':
    # Create and write initial values
    sys_var = shelve.open('sys_var.db')
    sys_var['uart_init'] = 'True'
    sys_var['apn_init'] = 'Error'
    sys_var.close()

    # Open db and read values
    sys_var = shelve.open('sys_var.db')
    print(sys_var['uart_init'])
    print(sys_var['apn_init'])
    sys_var.close()
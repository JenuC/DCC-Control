from dccx import *
import time
dcc = DCCInterface(r"C:\Program Files (x86)\BH\DCC\DLL\dcc64.dll")
result = dcc.init("C:\Program Files (x86)\BH\DCC\dcc100.ini")
if result != 0:
    error_code, error_message = dcc.get_error_string(result)
    print(f"Error initializing: {error_message}")


print(dcc.test_if_active(1))
print(dcc.test_if_active(0))

r, mod_info = dcc.get_module_info(1)
mod_info.print_fields() ## byte coding for the serial number needs fix
print("Mode:",dcc.get_mode())
#r = dcc.set_mode(0,force_use=0) ## cant get this working without error
print("Mode set 1,1:",r, dcc.get_mode())
print("Active :",dcc.test_if_active(1))
result, mod_info = dcc.get_module_info(1)
print("MODULEINFO:", result)
mod_info.print_fields()


r = dcc.set_parameter(1,dcc_params.C3_P12V,1,True)
print("C3_P12V",r)
#r = dcc.set_parameter(1,dcc_params.C3_P5V,1,True)
r = dcc.set_parameter(1,dcc_params.C3_GAIN_HV,1,70.0)
print("C3_GAIN_HV",r)
r = dcc.enable_outputs(1,True)
print("Enable",r)
# if dcc.get_overload_state(1)[1]>0:
#     dcc.clear_overload(1)
#     print(dcc.get_overload_state(1)[1])
print(dcc.get_parameter(1,dcc_params.C3_GAIN_HV))

#print(dcc.enable_outputs(1,False))
#print(dcc.get_init_status(1))
#print(dcc.get_gain_hv_limit(1,18))
#dcc.set_mode(0,1)
time.sleep(10)
print("Active :",dcc.test_if_active(1))
print("Mode:",dcc.get_mode())
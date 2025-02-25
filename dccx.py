from ctypes import *
from dataclasses import dataclass
from typing import Tuple
import os


from collections import namedtuple

# Define a named tuple to store the DCC parameters
DCCParameters = namedtuple('DCCParameters', [
    "DCC_ACTIVE", "PCI_BUS_NO", "C1_P5V", "C1_M5V", "C1_P12V", "C1_GAIN_HV",
    "C2_P5V", "C2_M5V", "C2_P12V", "C2_DIGOUT", "C3_COOLING", "C3_COOLVOLT",
    "C3_COOLCURR", "C3_GAIN_HV", "C3_P5V", "C3_M5V", "C3_P12V"
])

# Create an instance of DCCParameters with the same values as the original dictionary
dcc_params = DCCParameters(
    DCC_ACTIVE=0, PCI_BUS_NO=1, C1_P5V=2, C1_M5V=3, C1_P12V=4, C1_GAIN_HV=5,
    C2_P5V=6, C2_M5V=7, C2_P12V=8, C2_DIGOUT=9, C3_COOLING=10, C3_COOLVOLT=11,
    C3_COOLCURR=12, C3_GAIN_HV=13, C3_P5V=14, C3_M5V=15, C3_P12V=16
)


# Define the structures that match the C structs
class DCCModInfo(Structure):
    _fields_ = [
        ("module_type", c_short),
        ("bus_number", c_short),
        ("slot_number", c_short),
        ("base_adr", c_short),
        ("serial_no", c_char * 12),
        ("in_use", c_short)
    ]

    def print_fields(self):
        print("DCCModInfo:")
        print(f"  Module Type: {self.module_type}")
        print(f"  Bus Number: {self.bus_number}")
        print(f"  Slot Number: {self.slot_number}")
        print(f"  Base Address: {self.base_adr}")
        print(f"  Serial Number: {self.serial_no}")#{self.serial_no.decode('utf-8')}")
        print(f"  In Use: {self.in_use}")

class DCCdata(Structure):
    _fields_ = [
        ("gain_p5v", c_float),
        ("gain_m5v", c_float),
        ("gain_p12v", c_float),
        ("gain_hv", c_float),
        ("digi_out", c_ubyte),
        ("cooling", c_short),
        ("cool_voltage", c_float),
        ("cool_curr_lmt", c_float)
    ]

    def print_fields(self):
        print("DCCdata:")
        print(f"  +5V Gain: {self.gain_p5v:.3f}V")
        print(f"  -5V Gain: {self.gain_m5v:.3f}V")
        print(f"  +12V Gain: {self.gain_p12v:.3f}V")
        print(f"  HV Gain: {self.gain_hv:.3f}V")
        print(f"  Digital Out: {self.digi_out}")
        print(f"  Cooling: {self.cooling}")
        print(f"  Cooling Voltage: {self.cool_voltage:.3f}V")
        print(f"  Cooling Current Limit: {self.cool_curr_lmt:.3f}A")

class DCC_EEP_Data(Structure):
    _fields_ = [
        ("serial_no", c_char * 8),
        ("module_type", c_short),
        ("gain_p5v_limit", c_float),
        ("gain_m5v_limit", c_float),
        ("gain_p12v_limit", c_float),
        ("gain_hv_limit", c_float),
        ("cool_voltage_limit", c_float),
        ("cool_curr_limit", c_float)
    ]

    def print_fields(self):
        print("DCC EEPROM Data:")
        print(f"  Serial Number: {self.serial_no.decode('utf-8')}")
        print(f"  Module Type: {self.module_type}")
        print(f"  +5V Gain Limit: {self.gain_p5v_limit:.3f}V")
        print(f"  -5V Gain Limit: {self.gain_m5v_limit:.3f}V")
        print(f"  +12V Gain Limit: {self.gain_p12v_limit:.3f}V")
        print(f"  HV Gain Limit: {self.gain_hv_limit:.3f}V")
        print(f"  Cooling Voltage Limit: {self.cool_voltage_limit:.3f}V")
        print(f"  Cooling Current Limit: {self.cool_curr_limit:.3f}A")

class DCCInterface:
    """Interface to the DCC DLL functions"""
    
    def __init__(self, dll_path: str = "dcc100.dll"):
        """Initialize the DCC interface with the specified DLL path"""
        if not os.path.exists(dll_path):
            raise FileNotFoundError(f"DCC DLL not found at {dll_path}")
            
        self.dll = CDLL(dll_path)
        self._setup_function_prototypes()

    def _setup_function_prototypes(self):
        """Setup the function prototypes for the DLL calls"""
        
        # DCC_init
        self.dll.DCC_init.argtypes = [c_char_p]
        self.dll.DCC_init.restype = c_short

        # DCC_test_if_active
        self.dll.DCC_test_if_active.argtypes = [c_short]
        self.dll.DCC_test_if_active.restype = c_short

        # DCC_get_init_status
        self.dll.DCC_get_init_status.argtypes = [c_short, POINTER(c_short)]
        self.dll.DCC_get_init_status.restype = c_short

        # DCC_get_mode
        self.dll.DCC_get_mode.argtypes = []
        self.dll.DCC_get_mode.restype = c_short

        # DCC_set_mode
        self.dll.DCC_set_mode.argtypes = [c_short, c_short, POINTER(c_short)]
        self.dll.DCC_set_mode.restype = c_short

        # DCC_get_module_info
        self.dll.DCC_get_module_info.argtypes = [c_short, POINTER(DCCModInfo)]
        self.dll.DCC_get_module_info.restype = c_short

        # DCC_get_error_string
        self.dll.DCC_get_error_string.argtypes = [c_short, c_char_p, c_short]
        self.dll.DCC_get_error_string.restype = c_short

        # DCC_get_parameter
        self.dll.DCC_get_parameter.argtypes = [c_short, c_short, POINTER(c_float)]
        self.dll.DCC_get_parameter.restype = c_short

        # DCC_set_parameter
        self.dll.DCC_set_parameter.argtypes = [c_short, c_short, c_short, c_float]
        self.dll.DCC_set_parameter.restype = c_short

        # DCC_get_parameters
        self.dll.DCC_get_parameters.argtypes = [c_short, POINTER(DCCdata)]
        self.dll.DCC_get_parameters.restype = c_short

        # DCC_set_parameters
        self.dll.DCC_set_parameters.argtypes = [c_short, c_short, POINTER(DCCdata)]
        self.dll.DCC_set_parameters.restype = c_short

        # DCC_get_eeprom_data
        self.dll.DCC_get_eeprom_data.argtypes = [c_short, POINTER(DCC_EEP_Data)]
        self.dll.DCC_get_eeprom_data.restype = c_short

        # DCC_write_eeprom_data
        self.dll.DCC_write_eeprom_data.argtypes = [c_short, c_ushort, POINTER(DCC_EEP_Data)]
        self.dll.DCC_write_eeprom_data.restype = c_short

        # DCC_get_gain_HV_limit
        self.dll.DCC_get_gain_HV_limit.argtypes = [c_short, c_short, POINTER(c_short)]
        self.dll.DCC_get_gain_HV_limit.restype = c_short

        # DCC_set_gain_HV_limit
        self.dll.DCC_set_gain_HV_limit.argtypes = [c_short, c_short, POINTER(c_short)]
        self.dll.DCC_set_gain_HV_limit.restype = c_short

        # DCC_enable_outputs
        self.dll.DCC_enable_outputs.argtypes = [c_short, c_short]
        self.dll.DCC_enable_outputs.restype = c_short

        # DCC_clear_overload
        self.dll.DCC_clear_overload.argtypes = [c_short]
        self.dll.DCC_clear_overload.restype = c_short

        # DCC_get_overload_state
        self.dll.DCC_get_overload_state.argtypes = [c_short, POINTER(c_short)]
        self.dll.DCC_get_overload_state.restype = c_short

        # DCC_get_curr_lmt_state
        self.dll.DCC_get_curr_lmt_state.argtypes = [c_short, POINTER(c_short)]
        self.dll.DCC_get_curr_lmt_state.restype = c_short

    def init(self, ini_file: str) -> int:
        """Initialize the DCC module"""
        return self.dll.DCC_init(ini_file.encode('utf-8'))

    def test_if_active(self, mod_no: int) -> int:
        """Test if a module is active"""
        return self.dll.DCC_test_if_active(mod_no)

    def get_init_status(self, mod_no: int) -> Tuple[int, int]:
        """Get initialization status of a module"""
        status = c_short()
        result = self.dll.DCC_get_init_status(mod_no, byref(status))
        return result, status.value

    def get_mode(self) -> int:
        """Get current mode"""
        return self.dll.DCC_get_mode()

    def set_mode(self, mode: int, force_use: int) -> Tuple[int, int]:
        """Set mode with force option"""
        in_use = c_short()
        result = self.dll.DCC_set_mode(mode, force_use, byref(in_use))
        return result, in_use.value

    def get_module_info(self, mod_no: int) -> Tuple[int, DCCModInfo]:
        """Get module information"""
        info = DCCModInfo()
        result = self.dll.DCC_get_module_info(mod_no, byref(info))
        return result, info

    def get_error_string(self, error_id: int, max_length: int = 512) -> Tuple[int, str]:
        """Get error string for an error ID"""
        buffer = create_string_buffer(max_length)
        result = self.dll.DCC_get_error_string(error_id, buffer, max_length)
        return result, buffer.value.decode('utf-8')

    def get_parameter(self, mod_no: int, par_id: int) -> Tuple[int, float]:
        """Get parameter value"""
        value = c_float()
        result = self.dll.DCC_get_parameter(mod_no, par_id, byref(value))
        return result, value.value

    def set_parameter(self, mod_no: int, par_id: int, send_to_hard: int, value: float) -> int:
        """Set parameter value"""
        return self.dll.DCC_set_parameter(mod_no, par_id, send_to_hard, c_float(value))

    def get_parameters(self, mod_no: int) -> Tuple[int, DCCdata]:
        """Get all parameters"""
        data = DCCdata()
        result = self.dll.DCC_get_parameters(mod_no, byref(data))
        return result, data

    def set_parameters(self, mod_no: int, send_to_hard: int, data: DCCdata) -> int:
        """Set all parameters"""
        return self.dll.DCC_set_parameters(mod_no, send_to_hard, byref(data))

    def get_eeprom_data(self, mod_no: int) -> Tuple[int, DCC_EEP_Data]:
        """Get EEPROM data"""
        data = DCC_EEP_Data()
        result = self.dll.DCC_get_eeprom_data(mod_no, byref(data))
        return result, data

    def write_eeprom_data(self, mod_no: int, write_enable: int, data: DCC_EEP_Data) -> int:
        """Write EEPROM data"""
        return self.dll.DCC_write_eeprom_data(mod_no, write_enable, byref(data))

    def get_gain_hv_limit(self, mod_no: int, lim_id: int) -> Tuple[int, int]:
        """Get gain HV limit"""
        value = c_short()
        result = self.dll.DCC_get_gain_HV_limit(mod_no, lim_id, byref(value))
        return result, value.value

    def set_gain_hv_limit(self, mod_no: int, lim_id: int, value: int) -> int:
        """Set gain HV limit"""
        val = c_short(value)
        return self.dll.DCC_set_gain_HV_limit(mod_no, lim_id, byref(val))

    def enable_outputs(self, mod_no: int, enable: bool) -> int:
        """Enable/disable outputs"""
        return self.dll.DCC_enable_outputs(mod_no, 1 if enable else 0)

    def clear_overload(self, mod_no: int) -> int:
        """Clear overload state"""
        return self.dll.DCC_clear_overload(mod_no)

    def get_overload_state(self, mod_no: int) -> Tuple[int, int]:
        """Get overload state"""
        state = c_short()
        result = self.dll.DCC_get_overload_state(mod_no, byref(state))
        return result, state.value

    def get_curr_lmt_state(self, mod_no: int) -> Tuple[int, int]:
        """Get current limit state"""
        state = c_short()
        result = self.dll.DCC_get_curr_lmt_state(mod_no, byref(state))
        return result, state.value
    
    def print_all_parameters(self, mod_no: int):
        """Print all available parameters for a given module"""
        print(f"\nPrinting all parameters for module {mod_no}:")
        print("-" * 50)
        
        # Print module info
        result, mod_info = self.get_module_info(mod_no)
        if result == 0:
            mod_info.print_fields()
        else:
            print(f"Error getting module info: {result}")
        
        # Print current parameters
        result, data = self.get_parameters(mod_no)
        if result == 0:
            data.print_fields()
        else:
            print(f"Error getting parameters: {result}")
        
        # Print EEPROM data
        result, eep_data = self.get_eeprom_data(mod_no)
        if result == 0:
            eep_data.print_fields()
        else:
            print(f"Error getting EEPROM data: {result}")
        
        # Print current states
        result, overload = self.get_overload_state(mod_no)
        if result == 0:
            print("\nStates:")
            print(f"  Overload State: {overload}")
        
        result, curr_lmt = self.get_curr_lmt_state(mod_no)
        if result == 0:
            print(f"  Current Limit State: {curr_lmt}")
        
        print("-" * 50)
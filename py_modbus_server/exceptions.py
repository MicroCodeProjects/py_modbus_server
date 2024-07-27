class InvalidSlaveError(Exception):
    
    def __init__(self, slave_id: int):
        
        message = f"The slave id {slave_id} is not valid."
        Exception.__init__(self, message)
        
        
class InvalidRegisterTypeError(Exception):
    
    def __init__(self, register_type: str):
        
        message = f"The register type {register_type} is not valid."
        Exception.__init__(self, message)
        
        
class InvalidAddressError(Exception):
    
    def __init__(self, address: int):
        
        message = f"The address {address} is not valid."
        Exception.__init__(self, message)


class InvalidNameError(Exception):
    
    def __init__(self, name: str):
        
        message = f"The name {name} is not valid."
        Exception.__init__(self, message)
        
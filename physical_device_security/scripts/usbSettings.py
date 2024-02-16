import subprocess
import sys

def list_usb_devices():
    try:
        # Run usbguard list-devices to list USB devices
        result = subprocess.run(['usbguard', 'list-devices'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise Exception(result.stderr)

        usb_devices = {}
        lines = result.stdout.split('\n')

        for line in lines:
            if 'id' in line:
                parts = line.split()
                usb_id = parts[3]
                usb_status = parts[1]  # 'allow' or 'deny'
                usb_name = ' '.join(parts[7:9])
                usb_serial = parts[5] if 'serial' in parts else ''
                
                # Add the USB device to the dictionary
                usb_devices[usb_id] = {
                    'name': usb_name,
                    'serial': usb_serial,
                    'enabled': usb_status == 'allow'
                }

        return usb_devices

    except Exception as e:
        print(f"Error listing USB devices: {e}")
        sys.exit(1)

def allow_usb_device(device_id):
    try:
        # Run usbguard allow-device to allow a specific USB device
        result = subprocess.run(['sudo', 'usbguard', 'allow-device', device_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(f"USB device {device_id} allowed.")
        else:
            raise Exception(result.stderr)
    except Exception as e:
        print(f"Error allowing USB device: {e}")

def block_usb_device(device_id):
    try:
        # Run usbguard block-device to block a specific USB device
        result = subprocess.run(['sudo', 'usbguard', 'block-device', device_id], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode == 0:
            print(f"USB device {device_id} blocked.")
        else:
            raise Exception(result.stderr)
    except Exception as e:
        print(f"Error blocking USB device: {e}")

def main():
    # List USB devices
    usb_devices = list_usb_devices()
    print("USB Devices:")
    print(usb_devices)

    allow_usb_device('1d6b:0002')

    # # Input: USB device ID to allow or block
    # device_id = input("Enter the USB device ID to allow/block: ")

    # # Input: Action - allow or block
    # action = input("Enter 'allow' to allow or 'block' to block: ")

    # # Allow or block USB device
    # if action == 'allow':
    #     allow_usb_device(device_id)
    # elif action == 'block':
    #     block_usb_device(device_id)
    # else:
    #     print("Invalid action. Please enter 'allow' or 'block'.")

if __name__ == "__main__":
    main()

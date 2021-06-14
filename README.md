## OAuth
- no API calls exposed on power devices
- power devices use Google OAuth API (or other vendor's implementation) to identify itself and set up authorization
- devices will then poll the authorization server on each interaction to verify grant or deny status
- sample implementation: https://developers.google.com/identity/protocols/oauth2/limited-input-device


## Open API calls:

GetDeviceDetails
- Input: N/A
- Output: XML summary of device details including manufacturer, device type, model number, serial number, etc.
Sample: https://www.panasonic.com/my/consumer/home-appliances/refrigerator/2-door/nr-bv328xs.specs.html

GetPowerUsageSummary
- Input: N/A
- Output: XML summary of device's power usage. This can be of whatever device supports, either dynamically captured since device
  startup, or including details from static storage as well.

GetPowerUsageDetails
- Input: N/A (TBD: Shall we support requesting time interval?)
- Output: XML list of current power usage details in time series

GetDeviceType
- Input: N/A
- Output: XML summary of what kind of device this is (eg. "refrigerator", "television", "air conditioner"). Can have multiple names
  in cases of aliases (eg. "fridge", "tv").

GetPowerRatingsInfo
- Summary: Display power ratings specifications for device as provided by manufacturer.
- Input: N/A
- Output: XML summary of power ratings (Energy Consumption in kWh/year; Energy Level (n/5 Stars); Voltage, Watts, Hertz)

IsEcoModeSupported
- Input: N/A
- Output: "Supported", "Supported:HWOnly", or "NotSupported", depending if device has some kind of of Eco mode (which can be controlled either
  physically on device by hardware switch, or by API power control calls (SetEcoModeOn, SetEcoModeOff).

SetEcoModeOn
- Summary: Instructs device to reduce its power consumption to Eco Mode (eg. reduce processing speed, cooling, functionality, etc.) to reduce
  power consumption.
- Input: N/A
- Output: "EcoModeOn", or "NotSupported"

SetEcoModeOff
- Summary: Instructs device to disable Eco Mode, aka return to "full power" mode. Can be similar as "SetToDefaultMode".
- Input: N/A
- Output: "EcoModeOff", or "NotSupported"

SetToDefaultMode
- Summary: Instructs device to reset its power consumption to device default.
- Input: N/A
- Output: "DefaultMode", or "NotSupported"

SetPowerStandbyMode
- Summary: Instructs device to power itself down to standby mode. Only bare minimal power consumption in this mode.
- Input: N/A
- Output: "StandbyMode", or "NotSupported"

SetPowerActiveMode
- Summary: Instructs device to power itself up, in normal power consumption mode.
- Input: N/A
- Output: "ActiveMode", or "NotSupported"

GetFactoryInitTimeGMT
- Input: N/A
- Output: The Date/Time the device was made factory ready; "yyyy-mm-dd hh:mm:ss" in GMT, or "NotSupported"

GetFactoryInitTimeLocal
- Input: N/A
- Output: The Date/Time the device was made factory ready: "yyyy-mm-dd hh:mm:ss; {TimeZone string}", or "NotSupported"

GetNTPService
- Input: N/A
- Output: The DNS:Port details of NTP service device is using to calibrate time, or "NotSupported"

SetNTPService
- Input: The DNS:Port details of NTP service that device should use to calibrate time
- Output: "Success: {DNS:Port details of NTP service}", or "NotSupported"

GetCurrentTimeGMT
- Input: N/A
- Output: The current Date/Time of the device in GMT: "yyyy-mm-dd hh:mm:ss", or "NotSupported"

SetCurrentTimeGMT
- Input: The Date/Time that the device should be set to, in GMT: "yyyy-mm-dd hh:mm:ss"
- Output: "yyyy-mm-dd hh:mm:ss", or "Error:NTPActive", or "NotSupported"

GetTimeLocal
- Input: N/A
- Output: "yyyy-mm-dd hh:mm:ss; {TimeZone string}", or "NotSupported"

SetTimeLocal
- Input: The Date/Time that the device should be set to, specified in local time: "yyyy-mm-dd hh:mm:ss"
- Output: "Success: yyyy-mm-dd hh:mm:ss; {TimeZone string}", or "Error:NTPActive", or "NotSupported"

GetTimeZone
- Input: N/A
- Output: "{TimeZone string}, or "NotSupported"

SetTimeZone
- Input: TimeZone string to set (eg. "Tokyo;+9")
- Output: "Success: {TimeZone string}", or "NotSupported"


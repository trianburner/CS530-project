# WVLKWY

## CS530-Project

Hardware project involving Raspberry Pi Pico W, HCSR04 ultrasonic sensors, a Flutter application, and NeoPixels. Designed to turn on lights when motion is detected. Light color and alarm time are adjustable via the Flutter application. 

## DEMO Video
Check out our demo of the hardware here:
[![YouTube thumbnail](./Images/thumb.jpg)]()
## Project Structure
```
$PROJECT_ROOT
 +---flutter_wlkway
|   |   main.dart
|   |   
|   +---system
|   |       AppData.dart
|   |       Connection.dart
|   |       Networking.dart
|   |       notification_service.dart
|   |       theme_provider.dart
|   |       
|   \---widgets
|       |   .DS_Store
|       |   Base.dart
|       |   
|       +---buttons
|       |       ChangeThemeButton.dart
|       |       
|       \---pages
|               .DS_Store
|               Connections.dart
|               Manage.dart
|               
 +---Images
|       thumb.jpg
|       
\---pico_w_wlkway
    +---src
    |       alarm.py
    |       hcsr04.py
    |       lights.py
    |       main.py
    |       
    \---tests
            test_client.py
```
## License

Apache License

Check out [LICENSE](./LICENSE) for more detail.

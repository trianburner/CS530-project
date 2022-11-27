import 'package:flutter_local_notifications/flutter_local_notifications.dart';

class NotificationService {
  static final notifs = FlutterLocalNotificationsPlugin();

  static Future<void> init() async {
    DarwinInitializationSettings iosSettings = DarwinInitializationSettings(
        requestAlertPermission: true,
        requestBadgePermission: true,
        requestSoundPermission: true,
        onDidReceiveLocalNotification: onDidReceiveNotification);

    await notifs.initialize(InitializationSettings(iOS: iosSettings));
  }

  static Future<NotificationDetails> _notifDetails() async {
    return NotificationDetails(iOS: DarwinNotificationDetails());
  }

  static Future<void> showNotif(
      {required int id, required String title, required String body}) async {
    final details = await _notifDetails();
    await notifs.show(id, title, body, details);
  }

  static void onDidReceiveNotification(
      int id, String? title, String? body, String? payload) {
    print('ID: $id | Title: $title | Body: $body');
  }
}

import 'package:flutter/material.dart';
import 'Connection.dart';
import 'Networking.dart';

class AppData extends InheritedWidget {
  final Data data;

  const AppData({
    Key? key,
    required this.data,
    required Widget child,
  }) : super(key: key, child: child);

  static AppData of(BuildContext context) {
    final AppData? result = context.dependOnInheritedWidgetOfExactType<AppData>();
    assert(result != null, 'No AppData found in context');
    return result!;
  }

  @override
  bool updateShouldNotify(AppData old) {
    return data == old.data;
  }
}

class Data {
  List<int> RGB = [255, 255, 255];
  List<TimeOfDay> alarmTimes = [TimeOfDay(hour: 0, minute: 0), TimeOfDay(hour: 6, minute: 0)];
  List<Connection> connections = [];
  int activeIndex = -1;

  void changeColor(BuildContext context, Color input) {
    RGB = [input.red, input.green, input.blue];
    sendColor(context);
  }

  void changeAlarm(BuildContext context, int indicator, TimeOfDay time) {
    // 0 - start, 1 - end
    alarmTimes[indicator] = time;
    sendAlarm(context);
  }

  void sendColor(BuildContext context) {
    Network.of(context).sendMessage("COLOR-${RGB[0]}-${RGB[1]}-${RGB[2]}");
  }

  void sendAlarm(BuildContext context) {
    Network.of(context).sendMessage("ALARM-${_formatTime(alarmTimes[0])}-${_formatTime(alarmTimes[1])}");
  }

  void initPresets(BuildContext context) {
    sendColor(context);
    sendAlarm(context);
  }

  String _formatTime(TimeOfDay input) {
    return "${input.hour.toString().padLeft(2, '0')}:${input.minute.toString().padLeft(2, '0')}";
  }
}
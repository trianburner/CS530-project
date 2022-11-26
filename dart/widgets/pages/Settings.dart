import 'package:flutter/material.dart';
import '../buttons/ChangeThemeButton.dart';
import 'package:toggle_switch/toggle_switch.dart';

class Settings extends StatefulWidget {
  const Settings({Key? key}) : super(key: key);

  @override
  _SettingsState createState() => _SettingsState();
}

class _SettingsState extends State<Settings> {
  bool notifsStatus = false;


  void setNotifs(bool command) {
      setState(() {
        notifsStatus = command;
      });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.all(5),
      child: Column(
        children: [
          Spacer(),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              Text("Enable Dark Mode"),
              ChangeThemeButtonWidget()
            ],
          ),
          Spacer(),
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              Text("Enable notifications"),
              Switch.adaptive(
                value: notifsStatus,
                onChanged: (value) {
                  setNotifs(value);
                },
              )
            ],
          ),
          Spacer()
        ],
      ),
    );
  }
}

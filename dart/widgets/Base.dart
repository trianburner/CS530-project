import 'package:flutter/material.dart';
import 'package:rbg_led/widgets/pages/Settings.dart';
import 'buttons/ChangeThemeButton.dart';
import 'pages/Connections.dart';
import 'pages/Manage.dart';

class Base extends StatefulWidget {
  const Base({Key? key, required this.title}) : super(key: key);

  final String title;

  @override
  State<Base> createState() => _BaseState();
}

class _BaseState extends State<Base> {
  int currIndex = 0;
  List<Widget> screens = [
    Connections(),
    Manage()
  ];

  @override
  void initState() {
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.title, textAlign: TextAlign.left),
        actions: [
          Row(
            children: [
              Icon(Icons.nightlight_round),
              ChangeThemeButtonWidget()
            ],
          )
        ],
      ),
      body: Center(
        child: screens[currIndex],
      ),
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: currIndex,
        onTap: (index) {
          setState(() {
            currIndex = index;
          });
        },
        items: [
          BottomNavigationBarItem(
              icon: Icon(Icons.private_connectivity), label: "Connections"),
          BottomNavigationBarItem(
              icon: Icon(Icons.verified_user), label: "Manage")
        ],
      ),
    );
  }
}
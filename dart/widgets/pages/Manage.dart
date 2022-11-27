import 'package:flutter/material.dart';
import 'package:flutter_colorpicker/flutter_colorpicker.dart';
import '../../system/AppData.dart';

class Manage extends StatefulWidget {
  const Manage({Key? key}) : super(key: key);

  @override
  _ManageState createState() => _ManageState();
}

class _ManageState extends State<Manage> {
  late Data data;
  late TimeOfDay start, end;
  late Color currColor, activeColor;

  @override
  void didChangeDependencies() {
    data = AppData.of(context).data;

    start = data.alarmTimes[0];
    end = data.alarmTimes[1];

    var rgb = data.RGB;
    currColor = Color.fromRGBO(rgb[0], rgb[1], rgb[2], 1);
    activeColor = currColor;

    super.didChangeDependencies();
  }

  void setColor(Color input) {
    setState(() {
      activeColor = input;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
        margin: EdgeInsets.all(15),
        child: Column(children: [
          Container(
            alignment: Alignment.centerLeft,
            width: double.infinity,
            child: Text("Alarm", style: TextStyle(fontSize: 24)),
          ),
          Container(
            margin: EdgeInsets.symmetric(horizontal: 15, vertical: 5),
            decoration: BoxDecoration(
                color: Colors.grey.shade200,
                borderRadius: BorderRadius.all(Radius.circular(15)),
                border: Border.all(color: Colors.grey.shade900)),
            child: Column(children: [
              Row(mainAxisAlignment: MainAxisAlignment.spaceEvenly, children: [
                Container(
                  padding: EdgeInsets.all(5),
                  child: Text("Starting Time",
                      style:
                          TextStyle(color: Colors.black, fontSize: 18, fontStyle: FontStyle.italic)),
                ),
                ElevatedButton(
                  child: Text(
                      '${start.hour.toString().padLeft(2, '0')}:${start.minute.toString().padLeft(2, '0')}'),
                  onPressed: () async {
                    TimeOfDay? newStart= await showTimePicker(initialEntryMode: TimePickerEntryMode.input,
                        context: context, initialTime: start);

                    if (newStart == null) {
                      return;
                    } else {
                      AppData.of(context).data.changeAlarm(context, 0, newStart);
                      setState(() {
                        start = newStart;
                      });
                    }
                  },
                )
              ]),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                children: [
                  Container(
                      padding: EdgeInsets.all(5),
                      child: Text("Ending Time",
                          style: TextStyle(color: Colors.black,
                              fontSize: 18, fontStyle: FontStyle.italic))),
                  ElevatedButton(
                    child: Text(
                        '${end.hour.toString().padLeft(2, '0')}:${end.minute.toString().padLeft(2, '0')}'),
                    onPressed: () async {
                      TimeOfDay? newEnd = await showTimePicker(initialEntryMode: TimePickerEntryMode.input,
                          context: context, initialTime: end);

                      if (newEnd == null) {
                        return;
                      } else {
                        AppData.of(context).data.changeAlarm(context, 1, newEnd);
                        setState(() {
                          end = newEnd;
                        });
                      }
                    },
                  )
                ],
              ),
            ]),
          ),
          Expanded(
            child:  Column(
              children: [
                Container(
                  margin: EdgeInsets.all(50),
                  alignment: Alignment.center,
                  width: 150,
                  height: 150,
                  padding: EdgeInsets.all(10),
                  decoration: BoxDecoration(
                      border: Border.all(color: Colors.black, width: 3),
                      color: currColor,
                      shape: BoxShape.circle),
                  child: Text(activeColor.toString(),
                      style: TextStyle(color: Colors.black)),
                ),
                ElevatedButton(
                  onPressed: () => showDialog(
                    context: context,
                    builder: (context) => AlertDialog(
                      content: SingleChildScrollView(
                        child: ColorPicker(
                          enableAlpha: false,
                          pickerColor: activeColor,
                          onColorChanged: setColor,
                        ),
                      ),
                      actions: [
                        TextButton(
                            onPressed: () {
                              Navigator.pop(context, false);
                            },
                            child: Text("Cancel")),
                        TextButton(
                            onPressed: () {
                              Navigator.pop(context, true);
                            },
                            child: Text("Select"))
                      ],
                    ),
                  ).then((confirm) {
                    if (confirm) {
                      AppData.of(context).data.changeColor(context, activeColor);
                      setState(() {
                        currColor = activeColor;
                        print("new color: " + currColor.toString());
                      });
                    } else {
                      activeColor = currColor;
                    }
                  }),
                  child: Text("Change color", style: TextStyle(fontSize: 16)),
                )
              ],
            ),
          )
        ]));
  }
}

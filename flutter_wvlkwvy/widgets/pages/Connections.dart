///
/// Connections.dart manages various IP addresses via Socket programming
/// 
/// If connections unsuccessful, Dialog prompted showing specific exception
/// 
import 'package:flutter/material.dart';
import '../../system/AppData.dart';
import '../../system/Connection.dart';
import '../../system/Networking.dart';

class Connections extends StatefulWidget {
  const Connections({Key? key}) : super(key: key);

  @override
  _ConnectionsState createState() => _ConnectionsState();
}

class _ConnectionsState extends State<Connections> {
  TextEditingController nameC = TextEditingController();
  TextEditingController ipC = TextEditingController();
  bool loading = false;
  Connection? focusConn;
  late Data data;

  @override
  void initState() {
    super.initState();
  }

  @override
  void didChangeDependencies() {
    data = AppData.of(context).data;
    super.didChangeDependencies();
  }

  ///
  /// isLoading() prompts loading screen 
  /// 
  void isLoading(bool status) {
    if (status) {
      showDialog(
          context: context,
          builder: (context) {
            return AlertDialog(
              title: Text(
                "Connecting",
                textAlign: TextAlign.center,
              ),
              content: Container(
                alignment: Alignment.center,
                width: 16,
                height: 16,
                child: CircularProgressIndicator(),
              ),
            );
          });
    } else {
      Navigator.pop(context);
    }
  }

  ///
  /// promptConnection() prompts dialog for setting new connection's values
  void promptConnection() {
    showDialog(
        barrierDismissible: true,
        context: context,
        builder: (context) => AlertDialog(
              content: SingleChildScrollView(
                child: Column(
                  children: [
                    TextField(
                      controller: nameC,
                      decoration: InputDecoration(hintText: "Device name"),
                    ),
                    TextField(
                        controller: ipC,
                        decoration:
                            InputDecoration(hintText: "Device's IP address")),
                    ElevatedButton(
                      onPressed: addConnection,
                      child: Text("Add device"),
                    )
                  ],
                ),
              ),
            )).then((_) {
      nameC.clear();
      ipC.clear();
    });
  }

  void addConnection() {
    setState(() {
      data.connections.add(Connection(name: nameC.text, ip: ipC.text));
      Navigator.pop(context);
    });
  }

  ///
  /// toggleConnection() allows for quick connection/disconnection 
  void toggleConnection(int index) async {
    isLoading(true);

    if (index != data.activeIndex) {
      try {
        disconnect();
        await Network.of(context).initClient(data.connections[index].ip);

        focusConn = data.connections[index];
        AppData.of(context).data.initPresets(context);

        setState(() {
          data.activeIndex = index;
        });
      } catch (e) {
        isLoading(false);

        // Invalid client
        showDialog(
          barrierDismissible: true,
          context: context,
          builder: (context) => AlertDialog(
            content: Container(
                margin: EdgeInsets.all(15), child: Text(e.toString())),
          ),
        );
        return;
      }
    } else {
      disconnect();
    }

    isLoading(false);
  }

  void setActive(int index) {
    data.activeIndex = index;
  }

  ///
  /// promptRemoval prompts user with Dialog on which connection to remove
  /// 
  void promptRemoval() {
    showDialog(
        barrierDismissible: true,
        context: context,
        builder: (context) => AlertDialog(
              content: SingleChildScrollView(
                child: Column(
                  children: [
                    Text("Choose which device to remove.",
                        textAlign: TextAlign.center),
                    Container(
                        padding: EdgeInsets.all(5),
                        child: StatefulBuilder(
                          builder: (context, dropDownState) {
                            return DropdownButton<Connection>(
                              isExpanded: true,
                              value: focusConn,
                              icon: const Icon(Icons.keyboard_arrow_down),
                              items: data.connections
                                  .map<DropdownMenuItem<Connection>>(
                                      (Connection cur) {
                                return DropdownMenuItem(
                                  value: cur,
                                  child: Text(cur.name),
                                );
                              }).toList(),
                              style: TextStyle(color: Colors.black),
                              onChanged: (Connection? val) {
                                dropDownState(() {
                                  focusConn = val;
                                });
                              },
                            );
                          },
                        )),
                    ElevatedButton(
                      onPressed: removeConnection,
                      child: Text("Remove device"),
                    )
                  ],
                ),
              ),
            ));
  }

  void removeConnection() async {
    disconnect();
    data.connections.remove(focusConn);
    focusConn = null;

    Navigator.pop(context);
  }

  void disconnect() {
    setState(() {
      data.activeIndex = -1;
      Network.of(context).initClient("");
    });
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: EdgeInsets.all(15),
      child: Column(
        children: [
          Row(
            children: [
              Text("Connections",
                  textAlign: TextAlign.left, style: TextStyle(fontSize: 24)),
              Spacer(),
              IconButton(
                onPressed: promptConnection,
                icon: Icon(Icons.add),
                splashRadius: 16,
              ),
              IconButton(
                onPressed: promptRemoval,
                icon: Icon(Icons.remove),
                splashRadius: 16,
              )
            ],
          ),
          Container(
              padding: EdgeInsets.all(5),
              decoration: BoxDecoration(
                  color: Colors.grey.shade200,
                  borderRadius: BorderRadius.all(Radius.circular(15)),
                  border: Border.all(color: Colors.grey.shade900)),
              child: data.connections.length == 0
                  ? Container(
                      alignment: Alignment.center,
                      width: double.infinity,
                      child: Text("No connections present.",
                          style: TextStyle(color: Colors.black)),
                    )
                  : ListView.builder(
                      shrinkWrap: true,
                      itemCount: data.connections.length,
                      itemBuilder: (context, index) {
                        Connection cur = data.connections[index];

                        return Card(
                          child: InkWell(
                              splashColor: Colors.blue,
                              onTap: () {
                                toggleConnection(index);
                              },
                              child: ListTile(
                                iconColor: index == data.activeIndex
                                    ? Colors.green
                                    : Colors.grey,
                                trailing: Icon(Icons.wifi),
                                title: Text(cur.name),
                                subtitle: Text(cur.ip),
                              )),
                        );
                      }))
        ],
      ),
    );
  }
}

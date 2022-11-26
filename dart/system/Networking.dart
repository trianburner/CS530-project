import 'dart:io';
import 'dart:typed_data';
import 'package:flutter/material.dart';

class Network extends InheritedWidget {
  Socket? client;

  Network({
    Key? key,
    required Widget child,
  }) : super(key: key, child: child);

  Future<void> initClient(String ip) async {
    if (ip == "") {
      sendMessage("!DISCONNECT");
      await client?.close();
      client = null;
    } else {
      client = await Socket.connect(ip, 5050).timeout(Duration(seconds: 15));
    }
  }

  bool validClient() {
    if (client == null) {
      print('Invalid client');
      return false;
    }
    return true;
  }

  void sendMessage(String msg) async {
    msg = msg.length.toString().padLeft(64, '0') + msg;

    if (validClient()) {
      client!.write(msg);
    }
  }

  static Network of(BuildContext context) {
    final Network? result =
        context.dependOnInheritedWidgetOfExactType<Network>();
    assert(result != null, 'No Network found in context');
    return result!;
  }

  @override
  bool updateShouldNotify(Network old) {
    return client != old.client;
  }
}

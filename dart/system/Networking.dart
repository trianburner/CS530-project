import 'dart:async';
import 'dart:io';
import 'notification_service.dart';
import 'dart:typed_data';
import 'package:flutter/material.dart';

class Network extends InheritedWidget {
  Socket? client;
  StreamSubscription? listener;

  Network({
    Key? key,
    required Widget child,
  }) : super(key: key, child: child) {
    NotificationService.init();
  }

  Future<void> initClient(String ip) async {
    if (ip == "") {
      sendMessage("!DISCONNECT");
      await client?.close();

      client = listener = null;
    } else {
      client = await Socket.connect(ip, 5050).timeout(Duration(seconds: 10));
      listener = listenToServer();
    }
  }

  StreamSubscription? listenToServer() {
    if (client != null) {
      return client!.listen(
        // handle data from the client
              (Uint8List data) async {
            final message = String.fromCharCodes(data);
            print(message);
            NotificationService.showNotif(id: 0,
                title: "ALERT",
                body: "Motion was recently detected near RGB lights.");
          },
          onError: (error) {
            print(error);
            client?.close();
          },
          onDone: () {
            print('Client left');
            client?.close();
          });
    } else {
      return null;
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

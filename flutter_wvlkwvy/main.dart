import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:rbg_led/system/AppData.dart';
import 'package:rbg_led/system/Networking.dart';
import 'system/theme_provider.dart';
import 'widgets/Base.dart';


void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({Key? key}) : super(key: key);

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return Network(
      child: AppData(
        data: Data(),
        child: ChangeNotifierProvider(
          create: (context) => ThemeProvider(),
          builder: (context, _) {
            final themeProvider = Provider.of<ThemeProvider>(context);

            return MaterialApp(
              title: 'RGB LED App',
              themeMode: themeProvider.themeMode,
              theme: MyThemes.lightTheme,
              darkTheme: MyThemes.darkTheme,
              home: const Base(title: 'RGB Manager'),
            );
          },
        ),
      ),
    );
  }
}

///
/// ThemeProvider.dart tracks current theme and implements new themes according to MyThemes
/// 
import 'package:flutter/material.dart';

class ThemeProvider extends ChangeNotifier {
  ThemeMode themeMode = ThemeMode.system;

  bool get isDarkMode => themeMode == ThemeMode.dark;

  void toggleTheme(bool isOn) {
    themeMode = isOn ? ThemeMode.dark : ThemeMode.light;
    notifyListeners();
  }
}

// custom Light & Dark themes
class MyThemes {
  static final darkTheme = ThemeData(
    scaffoldBackgroundColor: Colors.grey.shade900,
    colorScheme: ColorScheme.dark()
  );

  static final lightTheme = ThemeData(
    scaffoldBackgroundColor: Colors.white,
      colorScheme: ColorScheme.light()
  );
}

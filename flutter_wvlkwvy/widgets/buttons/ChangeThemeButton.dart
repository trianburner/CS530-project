///
/// changeThemeButtonWidget implements switch allowing for DarkMode vs LightMode
import 'package:flutter/material.dart';
import '../../system/theme_provider.dart';
import 'package:provider/provider.dart';

class ChangeThemeButtonWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final themeProvider = Provider.of<ThemeProvider>(context);

    return Switch.adaptive(
      inactiveTrackColor: Colors.black.withOpacity(0.5),
      value: themeProvider.isDarkMode,
      onChanged: (value) {
        themeProvider.toggleTheme(value);
    });
  }
}
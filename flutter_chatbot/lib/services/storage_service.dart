import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/chat.dart';
import '../utils/constants.dart';

class StorageService {
  static Future<List<Chat>> loadChats() async {
    final prefs = await SharedPreferences.getInstance();
    final chatsJson = prefs.getString(Constants.chatsStorageKey);

    if (chatsJson == null) return [];

    final chatsList = jsonDecode(chatsJson) as List;
    return chatsList.map((json) => Chat.fromJson(json)).toList();
  }

  static Future<void> saveChats(List<Chat> chats) async {
    final prefs = await SharedPreferences.getInstance();
    final chatsJson = jsonEncode(chats.map((chat) => chat.toJson()).toList());
    await prefs.setString(Constants.chatsStorageKey, chatsJson);
  }

  static Future<void> saveApiKey(String apiKey) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(Constants.apiKeyStorageKey, apiKey);
  }

  static Future<String?> loadApiKey() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(Constants.apiKeyStorageKey);
  }
}

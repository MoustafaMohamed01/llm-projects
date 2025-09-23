import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
import '../models/tool_model.dart';

class ChatService {
  static const String _chatHistoryKey = 'chat_history';

  Future<void> saveChatHistory(
      String toolId, List<ChatMessage> messages) async {
    final prefs = await SharedPreferences.getInstance();
    final allChats = await getAllChats();
    allChats[toolId] = messages.map((m) => m.toJson()).toList();
    await prefs.setString(_chatHistoryKey, jsonEncode(allChats));
  }

  Future<List<ChatMessage>> getChatHistory(String toolId) async {
    final allChats = await getAllChats();
    final chatData = allChats[toolId] as List<dynamic>? ?? [];
    return chatData.map((data) => ChatMessage.fromJson(data)).toList();
  }

  Future<Map<String, dynamic>> getAllChats() async {
    final prefs = await SharedPreferences.getInstance();
    final chatHistoryString = prefs.getString(_chatHistoryKey);
    if (chatHistoryString == null) return {};

    try {
      return jsonDecode(chatHistoryString) as Map<String, dynamic>;
    } catch (e) {
      return {};
    }
  }

  Future<void> clearChatHistory(String toolId) async {
    final prefs = await SharedPreferences.getInstance();
    final allChats = await getAllChats();
    allChats.remove(toolId);
    await prefs.setString(_chatHistoryKey, jsonEncode(allChats));
  }

  Future<void> clearAllChats() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_chatHistoryKey);
  }

  String exportChatHistory(List<ChatMessage> messages) {
    final buffer = StringBuffer();
    buffer.writeln('Chat Export - ${DateTime.now().toIso8601String()}');
    buffer.writeln('=' * 50);

    for (final message in messages) {
      final role = message.isUser ? 'You' : 'Assistant';
      buffer.writeln('\n[$role - ${message.timestamp.toString()}]');
      buffer.writeln(message.content);
      buffer.writeln('-' * 30);
    }

    return buffer.toString();
  }
}

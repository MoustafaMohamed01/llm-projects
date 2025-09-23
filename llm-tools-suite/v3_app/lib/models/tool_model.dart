import 'package:flutter/material.dart';

class ToolModel {
  final String id;
  final String name;
  final IconData icon;
  final String description;
  final Color color;

  ToolModel({
    required this.id,
    required this.name,
    required this.icon,
    required this.description,
    required this.color,
  });
}

class ChatMessage {
  final String content;
  final bool isUser;
  final DateTime timestamp;
  final String? toolId;

  ChatMessage({
    required this.content,
    required this.isUser,
    required this.timestamp,
    this.toolId,
  });

  Map<String, dynamic> toJson() {
    return {
      'content': content,
      'isUser': isUser,
      'timestamp': timestamp.millisecondsSinceEpoch,
      'toolId': toolId,
    };
  }

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    return ChatMessage(
      content: json['content'] ?? '',
      isUser: json['isUser'] ?? false,
      timestamp: DateTime.fromMillisecondsSinceEpoch(json['timestamp'] ?? 0),
      toolId: json['toolId'],
    );
  }
}

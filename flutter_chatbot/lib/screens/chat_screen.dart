import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:uuid/uuid.dart';
import '../models/chat.dart';
import '../models/message.dart';
import '../services/gemini_service.dart';
import '../widgets/message_bubble.dart';
import '../widgets/chat_input.dart';

class ChatScreen extends StatefulWidget {
  final Chat chat;
  final Function(Chat) onChatUpdated;

  const ChatScreen({
    super.key,
    required this.chat,
    required this.onChatUpdated,
  });

  @override
  State<ChatScreen> createState() => _ChatScreenState();
}

class _ChatScreenState extends State<ChatScreen> {
  final ScrollController _scrollController = ScrollController();
  late Chat currentChat;
  bool isLoading = false;

  @override
  void initState() {
    super.initState();
    currentChat = widget.chat;
  }

  void _scrollToBottom() {
    if (_scrollController.hasClients) {
      _scrollController.animateTo(
        _scrollController.position.maxScrollExtent,
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeOut,
      );
    }
  }

  Future<void> _sendMessage(String text) async {
    if (text.trim().isEmpty) return;

    final userMessage = Message(
      id: const Uuid().v4(),
      text: text.trim(),
      isUser: true,
      timestamp: DateTime.now(),
    );

    setState(() {
      currentChat = currentChat.copyWith(
        messages: [...currentChat.messages, userMessage],
        title: currentChat.messages.isEmpty ? text.trim() : currentChat.title,
        updatedAt: DateTime.now(),
      );
      isLoading = true;
    });

    widget.onChatUpdated(currentChat);

    WidgetsBinding.instance.addPostFrameCallback((_) => _scrollToBottom());

    // Get AI response
    final response = await GeminiService.generateResponse(text);

    final aiMessage = Message(
      id: const Uuid().v4(),
      text: response,
      isUser: false,
      timestamp: DateTime.now(),
    );

    setState(() {
      currentChat = currentChat.copyWith(
        messages: [...currentChat.messages, aiMessage],
        updatedAt: DateTime.now(),
      );
      isLoading = false;
    });

    widget.onChatUpdated(currentChat);

    WidgetsBinding.instance.addPostFrameCallback((_) => _scrollToBottom());
  }

  String _formatChatContent() {
    final buffer = StringBuffer();
    buffer.writeln('Chat: ${currentChat.title}');
    buffer.writeln('Date: ${DateTime.now().toString().split('.')[0]}');
    buffer.writeln('=' * 50);
    buffer.writeln();

    for (final message in currentChat.messages) {
      final time =
          '${message.timestamp.hour.toString().padLeft(2, '0')}:${message.timestamp.minute.toString().padLeft(2, '0')}';
      final sender = message.isUser ? 'You' : 'AI Assistant';
      buffer.writeln('[$time] $sender:');
      buffer.writeln(message.text);
      buffer.writeln();
    }

    return buffer.toString();
  }

  Future<void> _downloadChat() async {
    if (currentChat.messages.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('No messages to download'),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    // For mobile, we show dialog to copy or share
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        backgroundColor: const Color(0xFF2C2C2C),
        title: const Text(
          'Export Chat',
          style: TextStyle(color: Colors.white),
        ),
        content: const Text(
          'Choose how you want to export this chat:',
          style: TextStyle(color: Colors.white70),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              _copyChat();
            },
            child: const Text('Copy to Clipboard'),
          ),
          TextButton(
            onPressed: () {
              Navigator.pop(context);
              _shareChat();
            },
            child: const Text('Share'),
          ),
        ],
      ),
    );
  }

  Future<void> _copyChat() async {
    if (currentChat.messages.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('No messages to copy'),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    try {
      final content = _formatChatContent();
      await Clipboard.setData(ClipboardData(text: content));

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Chat copied to clipboard!'),
            backgroundColor: Colors.green,
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Copy failed: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _shareChat() async {
    if (currentChat.messages.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('No messages to share'),
          backgroundColor: Colors.orange,
        ),
      );
      return;
    }

    try {
      final content = _formatChatContent();
      await Clipboard.setData(ClipboardData(text: content));

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text(
                'Chat copied to clipboard! You can now paste it in any app.'),
            backgroundColor: Colors.green,
            duration: Duration(seconds: 4),
          ),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Share failed: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          currentChat.title,
          overflow: TextOverflow.ellipsis,
        ),
        backgroundColor: const Color(0xFF1E1E1E),
        foregroundColor: Colors.white,
        elevation: 0,
        actions: [
          PopupMenuButton<String>(
            icon: const Icon(Icons.more_vert),
            color: const Color(0xFF2C2C2C),
            onSelected: (value) {
              switch (value) {
                case 'export':
                  _downloadChat();
                  break;
                case 'copy':
                  _copyChat();
                  break;
              }
            },
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'export',
                child: Row(
                  children: [
                    Icon(Icons.download, color: Colors.blue),
                    SizedBox(width: 8),
                    Text('Export Chat', style: TextStyle(color: Colors.white)),
                  ],
                ),
              ),
              const PopupMenuItem(
                value: 'copy',
                child: Row(
                  children: [
                    Icon(Icons.copy, color: Colors.green),
                    SizedBox(width: 8),
                    Text('Copy to Clipboard',
                        style: TextStyle(color: Colors.white)),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      body: Column(
        children: [
          Expanded(
            child: currentChat.messages.isEmpty
                ? const Center(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Icon(Icons.smart_toy, size: 64, color: Colors.grey),
                        SizedBox(height: 16),
                        Text(
                          'Start a conversation!',
                          style: TextStyle(fontSize: 18, color: Colors.grey),
                        ),
                      ],
                    ),
                  )
                : ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.all(16),
                    itemCount:
                        currentChat.messages.length + (isLoading ? 1 : 0),
                    itemBuilder: (context, index) {
                      if (index == currentChat.messages.length && isLoading) {
                        return MessageBubble(
                          message: Message(
                            id: 'loading',
                            text: 'Thinking...',
                            isUser: false,
                            timestamp: DateTime.now(),
                          ),
                          isLoading: true,
                        );
                      }
                      return MessageBubble(
                          message: currentChat.messages[index]);
                    },
                  ),
          ),
          ChatInput(onSendMessage: _sendMessage),
        ],
      ),
    );
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }
}

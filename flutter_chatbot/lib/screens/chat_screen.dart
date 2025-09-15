import 'package:flutter/material.dart';
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

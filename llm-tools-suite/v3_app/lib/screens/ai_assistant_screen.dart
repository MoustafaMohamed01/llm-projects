import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../models/tool_model.dart';
import '../services/chat_service.dart';
import '../services/gemini_service.dart';
import '../theme/app_theme.dart';
import '../widgets/loading_animation.dart';

class AIAssistantScreen extends StatefulWidget {
  const AIAssistantScreen({Key? key}) : super(key: key);

  @override
  State<AIAssistantScreen> createState() => _AIAssistantScreenState();
}

class _AIAssistantScreenState extends State<AIAssistantScreen> {
  final TextEditingController _messageController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final ChatService _chatService = ChatService();
  final GeminiService _geminiService = GeminiService();

  List<ChatMessage> _messages = [];
  bool _isLoading = false;
  static const String _toolId = 'ai-assistant';

  @override
  void initState() {
    super.initState();
    _loadChatHistory();
    if (_messages.isEmpty) {
      _messages.add(ChatMessage(
        content: "Hello! I'm your AI assistant. How can I help you today?",
        isUser: false,
        timestamp: DateTime.now(),
        toolId: _toolId,
      ));
    }
  }

  Future<void> _loadChatHistory() async {
    final history = await _chatService.getChatHistory(_toolId);
    setState(() {
      _messages = history;
    });
  }

  Future<void> _saveChatHistory() async {
    await _chatService.saveChatHistory(_toolId, _messages);
  }

  Future<void> _sendMessage() async {
    final message = _messageController.text.trim();
    if (message.isEmpty || _isLoading) return;

    final userMessage = ChatMessage(
      content: message,
      isUser: true,
      timestamp: DateTime.now(),
      toolId: _toolId,
    );

    setState(() {
      _messages.add(userMessage);
      _isLoading = true;
    });

    _messageController.clear();
    _scrollToBottom();

    try {
      final systemInstruction =
          "You are an AI assistant designed to provide professional, accurate information. Your responses should be formal, concise, and helpful, free from bias and ambiguity, and always grammatically correct.";
      final response = await _geminiService.generateResponse(message,
          systemInstruction: systemInstruction);

      final assistantMessage = ChatMessage(
        content: response,
        isUser: false,
        timestamp: DateTime.now(),
        toolId: _toolId,
      );

      setState(() {
        _messages.add(assistantMessage);
        _isLoading = false;
      });

      await _saveChatHistory();
    } catch (e) {
      setState(() {
        _isLoading = false;
        _messages.add(ChatMessage(
          content: "Sorry, I encountered an error: ${e.toString()}",
          isUser: false,
          timestamp: DateTime.now(),
          toolId: _toolId,
        ));
      });
    }

    _scrollToBottom();
  }

  void _scrollToBottom() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_scrollController.hasClients) {
        _scrollController.animateTo(
          _scrollController.position.maxScrollExtent,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      }
    });
  }

  Future<void> _clearChat() async {
    await _chatService.clearChatHistory(_toolId);
    setState(() {
      _messages = [
        ChatMessage(
          content: "Hello! I'm your AI assistant. How can I help you today?",
          isUser: false,
          timestamp: DateTime.now(),
          toolId: _toolId,
        )
      ];
    });
  }

  void _copyToClipboard(String text) {
    Clipboard.setData(ClipboardData(text: text));
    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(
        content: Text('Copied to clipboard'),
        backgroundColor: AppTheme.successColor,
        duration: Duration(seconds: 2),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Container(
          padding: const EdgeInsets.all(24),
          decoration: AppTheme.cardGradient,
          margin: const EdgeInsets.all(16),
          child: Column(
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppTheme.primaryBlue.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(
                      Icons.psychology,
                      color: AppTheme.primaryBlue,
                      size: 32,
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'AI Assistant',
                          style: Theme.of(context).textTheme.headlineSmall,
                        ),
                        const SizedBox(height: 4),
                        Text(
                          'I\'m here to assist you professionally. Ask your question below.',
                          style:
                              Theme.of(context).textTheme.bodyMedium?.copyWith(
                                    color: AppTheme.textSecondary,
                                  ),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),

        Expanded(
          child: Container(
            margin: const EdgeInsets.symmetric(horizontal: 16),
            decoration: AppTheme.cardGradient,
            child: Column(
              children: [
                Expanded(
                  child: ListView.builder(
                    controller: _scrollController,
                    padding: const EdgeInsets.all(16),
                    itemCount: _messages.length + (_isLoading ? 1 : 0),
                    itemBuilder: (context, index) {
                      if (index == _messages.length && _isLoading) {
                        return const Padding(
                          padding: EdgeInsets.all(16),
                          child: LoadingAnimation(),
                        );
                      }

                      final message = _messages[index];
                      return _buildMessageWidget(message);
                    },
                  ),
                ),

                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    border: Border(
                      top: BorderSide(
                        color: Colors.white.withOpacity(0.1),
                      ),
                    ),
                  ),
                  child: Row(
                    children: [
                      Expanded(
                        child: TextField(
                          controller: _messageController,
                          decoration: const InputDecoration(
                            hintText: 'Type your message...',
                            border: OutlineInputBorder(),
                          ),
                          maxLines: null,
                          textInputAction: TextInputAction.send,
                          onSubmitted: (_) => _sendMessage(),
                        ),
                      ),
                      const SizedBox(width: 12),
                      ElevatedButton(
                        onPressed: _isLoading ? null : _sendMessage,
                        child: _isLoading
                            ? const SizedBox(
                                width: 20,
                                height: 20,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  valueColor: AlwaysStoppedAnimation<Color>(
                                      Colors.white),
                                ),
                              )
                            : const Text('Send'),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
        ),

        Container(
          padding: const EdgeInsets.all(16),
          child: Row(
            children: [
              Expanded(
                child: OutlinedButton.icon(
                  onPressed: _clearChat,
                  icon: const Icon(Icons.clear_all),
                  label: const Text('Clear Chat'),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: AppTheme.errorColor,
                    side: const BorderSide(color: AppTheme.errorColor),
                  ),
                ),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: ElevatedButton.icon(
                  onPressed: () {
                    final export = _chatService.exportChatHistory(_messages);
                    _copyToClipboard(export);
                  },
                  icon: const Icon(Icons.download),
                  label: const Text('Export Chat'),
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildMessageWidget(ChatMessage message) {
    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!message.isUser) ...[
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: AppTheme.primaryBlue.withOpacity(0.2),
                borderRadius: BorderRadius.circular(20),
              ),
              child: const Icon(
                Icons.psychology,
                color: AppTheme.primaryBlue,
                size: 16,
              ),
            ),
            const SizedBox(width: 12),
          ],
          Expanded(
            child: Column(
              crossAxisAlignment: message.isUser
                  ? CrossAxisAlignment.end
                  : CrossAxisAlignment.start,
              children: [
                Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: message.isUser
                        ? AppTheme.primaryBlue
                        : Colors.white.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(16),
                    border: message.isUser
                        ? null
                        : Border.all(color: Colors.white.withOpacity(0.1)),
                  ),
                  constraints: BoxConstraints(
                    maxWidth: MediaQuery.of(context).size.width * 0.8,
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (message.isUser)
                        Text(
                          message.content,
                          style: const TextStyle(color: Colors.white),
                        )
                      else
                        MarkdownBody(
                          data: message.content,
                          styleSheet: MarkdownStyleSheet(
                            p: const TextStyle(color: AppTheme.textPrimary),
                            h1: const TextStyle(
                                color: AppTheme.primaryBlue,
                                fontWeight: FontWeight.bold),
                            h2: const TextStyle(
                                color: AppTheme.primaryBlue,
                                fontWeight: FontWeight.w600),
                            h3: const TextStyle(
                                color: AppTheme.primaryBlue,
                                fontWeight: FontWeight.w500),
                            strong: const TextStyle(
                                color: AppTheme.secondaryBlue,
                                fontWeight: FontWeight.bold),
                            em: const TextStyle(
                                color: AppTheme.primaryBlue,
                                fontStyle: FontStyle.italic),
                            code: TextStyle(
                              backgroundColor: Colors.black.withOpacity(0.3),
                              color: AppTheme.secondaryBlue,
                              fontFamily: 'monospace',
                            ),
                            codeblockDecoration: BoxDecoration(
                              color: Colors.black.withOpacity(0.3),
                              borderRadius: BorderRadius.circular(8),
                            ),
                          ),
                        ),
                      if (!message.isUser) ...[
                        const SizedBox(height: 8),
                        Row(
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            TextButton.icon(
                              onPressed: () =>
                                  _copyToClipboard(message.content),
                              icon: const Icon(Icons.copy, size: 16),
                              label: const Text('Copy'),
                              style: TextButton.styleFrom(
                                padding: const EdgeInsets.symmetric(
                                    horizontal: 8, vertical: 4),
                                minimumSize: Size.zero,
                                tapTargetSize: MaterialTapTargetSize.shrinkWrap,
                              ),
                            ),
                          ],
                        ),
                      ],
                    ],
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  _formatTimestamp(message.timestamp),
                  style: Theme.of(context).textTheme.bodySmall?.copyWith(
                        color: AppTheme.textSecondary.withOpacity(0.7),
                      ),
                ),
              ],
            ),
          ),
          if (message.isUser) ...[
            const SizedBox(width: 12),
            Container(
              padding: const EdgeInsets.all(8),
              decoration: BoxDecoration(
                color: AppTheme.primaryBlue.withOpacity(0.2),
                borderRadius: BorderRadius.circular(20),
              ),
              child: const Icon(
                Icons.person,
                color: AppTheme.primaryBlue,
                size: 16,
              ),
            ),
          ],
        ],
      ),
    );
  }

  String _formatTimestamp(DateTime timestamp) {
    final now = DateTime.now();
    final difference = now.difference(timestamp);

    if (difference.inMinutes < 1) {
      return 'Just now';
    } else if (difference.inHours < 1) {
      return '${difference.inMinutes}m ago';
    } else if (difference.inDays < 1) {
      return '${difference.inHours}h ago';
    } else {
      return '${difference.inDays}d ago';
    }
  }
}

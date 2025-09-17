import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../models/message.dart';

class MessageBubble extends StatelessWidget {
  final Message message;
  final bool isLoading;

  const MessageBubble({
    super.key,
    required this.message,
    this.isLoading = false,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 4),
      child: Row(
        mainAxisAlignment:
            message.isUser ? MainAxisAlignment.end : MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.end,
        children: [
          if (!message.isUser) ...[
            const CircleAvatar(
              radius: 16,
              backgroundColor: Color(0xFF2C2C2C),
              child:
                  Icon(Icons.smart_toy, size: 16, color: Colors.white70),
            ),
            const SizedBox(width: 8),
          ],
          Flexible(
            child: Container(
              padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
              decoration: BoxDecoration(
                color: message.isUser
                    ? Theme.of(context).colorScheme.primary
                    : const Color(0xFF2C2C2C),
                borderRadius: BorderRadius.circular(18),
              ),
              child: isLoading
                  ? Row(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        SizedBox(
                          width: 16,
                          height: 16,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                            valueColor: AlwaysStoppedAnimation<Color>(
                              Colors.grey[600]!,
                            ),
                          ),
                        ),
                        const SizedBox(width: 8),
                        Text(
                          message.text,
                          style: TextStyle(
                            color: Colors.grey[600],
                          ),
                        ),
                      ],
                    )
                  : message.isUser
                      ? Text(
                          message.text,
                          style: const TextStyle(color: Colors.white),
                        )
                      : MarkdownBody(
                          data: message.text,
                          styleSheet: MarkdownStyleSheet(
                            p: const TextStyle(
                              color: Colors.white70,
                              fontSize: 14,
                            ),
                            h1: const TextStyle(
                              color: Colors.white,
                              fontSize: 20,
                              fontWeight: FontWeight.bold,
                            ),
                            h2: const TextStyle(
                              color: Colors.white,
                              fontSize: 18,
                              fontWeight: FontWeight.bold,
                            ),
                            h3: const TextStyle(
                              color: Colors.white,
                              fontSize: 16,
                              fontWeight: FontWeight.bold,
                            ),
                            strong: const TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                            em: const TextStyle(
                              color: Colors.white70,
                              fontStyle: FontStyle.italic,
                            ),
                            code: const TextStyle(
                              backgroundColor: Color(0xFF3C3C3C),
                              color: Colors.greenAccent,
                              fontFamily: 'monospace',
                              fontSize: 12,
                            ),
                            codeblockDecoration: const BoxDecoration(
                              color: Color(0xFF1A1A1A),
                              borderRadius:
                                  BorderRadius.all(Radius.circular(8)),
                            ),
                            listBullet: const TextStyle(
                              color: Colors.white70,
                            ),
                            blockquote: const TextStyle(
                              color: Colors.white60,
                              fontStyle: FontStyle.italic,
                            ),
                            a: const TextStyle(
                              color: Colors.blueAccent,
                            ),
                          ),
                        ),
            ),
          ),
          if (message.isUser) ...[
            const SizedBox(width: 8),
            CircleAvatar(
              radius: 16,
              backgroundColor: Theme.of(context).colorScheme.primary,
              child: const Icon(Icons.person, size: 16, color: Colors.white),
            ),
          ],
        ],
      ),
    );
  }
}

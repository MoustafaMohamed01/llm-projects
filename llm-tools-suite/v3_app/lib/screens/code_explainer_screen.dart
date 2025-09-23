// lib/screens/code_explainer_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../services/gemini_service.dart';
import '../theme/app_theme.dart';

class CodeExplainerScreen extends StatefulWidget {
  const CodeExplainerScreen({Key? key}) : super(key: key);

  @override
  State<CodeExplainerScreen> createState() => _CodeExplainerScreenState();
}

class _CodeExplainerScreenState extends State<CodeExplainerScreen> {
  final TextEditingController _codeController = TextEditingController();
  final GeminiService _geminiService = GeminiService();

  String _selectedLanguage = 'Python';
  bool _isExplaining = false;
  String _explanation = '';

  final List<String> _languages = [
    'Python',
    'JavaScript',
    'Java',
    'C++',
    'C#',
    'Go',
    'Rust',
    'PHP',
    'Ruby',
    'Swift',
    'Kotlin',
    'TypeScript',
    'Other'
  ];

  Future<void> _explainCode() async {
    if (_codeController.text.trim().isEmpty) {
      _showSnackBar(
          'Please paste some code to explain.', AppTheme.warningColor);
      return;
    }

    setState(() {
      _isExplaining = true;
    });

    try {
      final prompt = '''You are a senior software engineer and code reviewer.

1. First, **print the entire $_selectedLanguage code snippet exactly as provided**, clearly labeled as 'Full Code:'.

2. Then provide a **comprehensive overview explanation** of what the entire code does.

3. Finally, give a **detailed, line-by-line explanation** of the code. For each line:
   - Explain what the line does.
   - Explain each key word, function, or syntax element.
   - Use bullet points or markdown formatting for clarity.
   - Explain context if part of a block (function, loop, condition).
   - Write lines in code blocks.

Here is the code:
```${_selectedLanguage.toLowerCase()}
${_codeController.text.trim()}
```

Start with the full code, then overview, then line-by-line explanation.''';

      final explanation = await _geminiService.generateResponse(prompt);

      setState(() {
        _explanation = explanation;
        _isExplaining = false;
      });

      _showSnackBar(
          'Code explanation generated successfully!', AppTheme.successColor);
    } catch (e) {
      setState(() {
        _isExplaining = false;
      });
      _showSnackBar(
          'Failed to explain code. Please try again.', AppTheme.errorColor);
    }
  }

  void _clearCode() {
    setState(() {
      _codeController.clear();
      _explanation = '';
    });
  }

  void _copyExplanation() {
    if (_explanation.isNotEmpty) {
      Clipboard.setData(ClipboardData(text: _explanation));
      _showSnackBar('Explanation copied to clipboard!', AppTheme.successColor);
    }
  }

  void _showSnackBar(String message, Color color) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(message),
        backgroundColor: color,
        duration: const Duration(seconds: 3),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Header
          Container(
            padding: const EdgeInsets.all(24),
            decoration: AppTheme.cardGradient,
            child: Column(
              children: [
                Row(
                  children: [
                    Container(
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.indigo.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Icon(
                        Icons.integration_instructions,
                        color: Colors.indigo,
                        size: 32,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Code Explainer',
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Understand code with AI-powered step-by-step explanations.',
                            style: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.copyWith(
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

          const SizedBox(height: 16),

          // Form
          Container(
            padding: const EdgeInsets.all(24),
            decoration: AppTheme.cardGradient,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Code Analysis',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const SizedBox(height: 4),
                Text(
                  'Get the full code snippet printed, plus a detailed overview and line-by-line explanation.',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: AppTheme.textSecondary,
                      ),
                ),
                const SizedBox(height: 24),

                // Programming Language Dropdown
                DropdownButtonFormField<String>(
                  value: _selectedLanguage,
                  decoration: const InputDecoration(
                    labelText: 'Programming Language',
                    prefixIcon: Icon(Icons.code),
                  ),
                  items: _languages.map((language) {
                    return DropdownMenuItem<String>(
                      value: language,
                      child: Row(
                        children: [
                          _getLanguageIcon(language),
                          const SizedBox(width: 8),
                          Text(language),
                        ],
                      ),
                    );
                  }).toList(),
                  onChanged: (value) {
                    setState(() {
                      _selectedLanguage = value!;
                    });
                  },
                ),

                const SizedBox(height: 16),

                // Code Input
                TextField(
                  controller: _codeController,
                  decoration: const InputDecoration(
                    labelText: 'Code to Explain',
                    hintText: 'Paste your code here...',
                    prefixIcon: Icon(Icons.code_outlined),
                    alignLabelWithHint: true,
                  ),
                  maxLines: 15,
                  style: const TextStyle(
                    fontFamily: 'monospace',
                    fontSize: 14,
                  ),
                ),

                const SizedBox(height: 24),

                // Action Buttons
                Row(
                  children: [
                    Expanded(
                      child: OutlinedButton.icon(
                        onPressed:
                            _codeController.text.isNotEmpty ? _clearCode : null,
                        icon: const Icon(Icons.clear),
                        label: const Text('Clear'),
                        style: OutlinedButton.styleFrom(
                          foregroundColor: AppTheme.errorColor,
                          side: const BorderSide(color: AppTheme.errorColor),
                          padding: const EdgeInsets.symmetric(vertical: 12),
                        ),
                      ),
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      flex: 2,
                      child: ElevatedButton.icon(
                        onPressed: _isExplaining ? null : _explainCode,
                        icon: _isExplaining
                            ? const SizedBox(
                                width: 16,
                                height: 16,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  valueColor: AlwaysStoppedAnimation<Color>(
                                      Colors.white),
                                ),
                              )
                            : const Icon(Icons.psychology),
                        label: Text(
                            _isExplaining ? 'Analyzing...' : 'Explain Code'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.indigo,
                          padding: const EdgeInsets.symmetric(vertical: 12),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),

          // Code Explanation Output
          if (_explanation.isNotEmpty) ...[
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(24),
              decoration: AppTheme.cardGradient,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'Code Explanation',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      ElevatedButton.icon(
                        onPressed: _copyExplanation,
                        icon: const Icon(Icons.copy),
                        label: const Text('Copy'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppTheme.successColor,
                          padding: const EdgeInsets.symmetric(
                            horizontal: 16,
                            vertical: 8,
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: 16),
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.white.withOpacity(0.05),
                      borderRadius: BorderRadius.circular(12),
                      border: Border.all(
                        color: Colors.white.withOpacity(0.1),
                      ),
                    ),
                    child: MarkdownBody(
                      data: _explanation,
                      styleSheet: MarkdownStyleSheet(
                        p: const TextStyle(
                          color: AppTheme.textPrimary,
                          height: 1.6,
                        ),
                        h1: const TextStyle(
                          color: AppTheme.primaryBlue,
                          fontWeight: FontWeight.bold,
                          fontSize: 24,
                        ),
                        h2: const TextStyle(
                          color: AppTheme.primaryBlue,
                          fontWeight: FontWeight.w600,
                          fontSize: 20,
                        ),
                        h3: const TextStyle(
                          color: AppTheme.primaryBlue,
                          fontWeight: FontWeight.w500,
                          fontSize: 18,
                        ),
                        strong: const TextStyle(
                          color: AppTheme.secondaryBlue,
                          fontWeight: FontWeight.bold,
                        ),
                        em: const TextStyle(
                          color: AppTheme.primaryBlue,
                          fontStyle: FontStyle.italic,
                        ),
                        code: TextStyle(
                          backgroundColor: Colors.black.withOpacity(0.4),
                          color: AppTheme.secondaryBlue,
                          fontFamily: 'monospace',
                          fontSize: 13,
                        ),
                        codeblockDecoration: BoxDecoration(
                          color: Colors.black.withOpacity(0.4),
                          borderRadius: BorderRadius.circular(8),
                          border: Border.all(
                            color: Colors.white.withOpacity(0.1),
                          ),
                        ),
                        listBullet: const TextStyle(
                          color: AppTheme.primaryBlue,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ),
          ],

          const SizedBox(height: 16),
        ],
      ),
    );
  }

  Widget _getLanguageIcon(String language) {
    IconData icon;
    Color color;

    switch (language.toLowerCase()) {
      case 'python':
        icon = Icons.auto_awesome;
        color = Colors.blue;
        break;
      case 'javascript':
      case 'typescript':
        icon = Icons.web;
        color = Colors.yellow;
        break;
      case 'java':
        icon = Icons.coffee;
        color = Colors.orange;
        break;
      case 'c++':
      case 'c#':
        icon = Icons.memory;
        color = Colors.purple;
        break;
      case 'swift':
        icon = Icons.phone_iphone;
        color = Colors.orange;
        break;
      case 'kotlin':
        icon = Icons.android;
        color = Colors.green;
        break;
      case 'go':
        icon = Icons.speed;
        color = Colors.cyan;
        break;
      case 'rust':
        icon = Icons.security;
        color = Colors.orange;
        break;
      case 'php':
        icon = Icons.web_asset;
        color = Colors.indigo;
        break;
      case 'ruby':
        icon = Icons.diamond;
        color = Colors.red;
        break;
      default:
        icon = Icons.code;
        color = Colors.grey;
        break;
    }

    return Icon(icon, color: color, size: 16);
  }
}

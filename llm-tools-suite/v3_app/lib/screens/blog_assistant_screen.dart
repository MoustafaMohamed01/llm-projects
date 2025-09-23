import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../services/gemini_service.dart';
import '../theme/app_theme.dart';

class BlogAssistantScreen extends StatefulWidget {
  const BlogAssistantScreen({Key? key}) : super(key: key);

  @override
  State<BlogAssistantScreen> createState() => _BlogAssistantScreenState();
}

class _BlogAssistantScreenState extends State<BlogAssistantScreen> {
  final TextEditingController _titleController = TextEditingController();
  final TextEditingController _keywordsController = TextEditingController();
  final GeminiService _geminiService = GeminiService();

  double _wordCount = 750;
  bool _isGenerating = false;
  String _generatedBlog = '';

  Future<void> _generateBlog() async {
    if (_titleController.text.trim().isEmpty ||
        _keywordsController.text.trim().isEmpty) {
      _showSnackBar('Please provide both a blog title and keywords.',
          AppTheme.warningColor);
      return;
    }

    setState(() {
      _isGenerating = true;
    });

    try {
      final prompt =
          '''Generate a comprehensive, well-structured, and engaging blog post.
**Title:** "${_titleController.text.trim()}"
**Keywords:** "${_keywordsController.text.trim()}" (Integrate these naturally throughout the content)
**Tone:** Professional yet accessible, suitable for a broad audience.
**Structure:** Include a captivating introduction, informative body paragraphs with clear headings/subheadings, and a concise conclusion (with a call to action if appropriate).
**Word Count:** Approximately ${_wordCount.toInt()} words.''';

      final response = await _geminiService.generateResponse(prompt);

      setState(() {
        _generatedBlog = response;
        _isGenerating = false;
      });

      _showSnackBar('Blog post generated successfully!', AppTheme.successColor);
    } catch (e) {
      setState(() {
        _isGenerating = false;
      });
      _showSnackBar('Failed to generate blog post. Please try again.',
          AppTheme.errorColor);
    }
  }

  void _copyToClipboard() {
    Clipboard.setData(ClipboardData(text: _generatedBlog));
    _showSnackBar('Blog copied to clipboard!', AppTheme.successColor);
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
                        color: Colors.orange.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Icon(
                        Icons.article,
                        color: Colors.orange,
                        size: 32,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Blog AI Assistant',
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Generate engaging blog posts with AI assistance.',
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
                  'Blog Configuration',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const SizedBox(height: 4),
                Text(
                  'Enter details of the blog you want to generate',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: AppTheme.textSecondary,
                      ),
                ),
                const SizedBox(height: 24),

                // Blog Title
                TextField(
                  controller: _titleController,
                  decoration: const InputDecoration(
                    labelText: 'Blog Title',
                    hintText: 'e.g., The Future of AI in Healthcare',
                  ),
                ),

                const SizedBox(height: 16),

                // Keywords
                TextField(
                  controller: _keywordsController,
                  decoration: const InputDecoration(
                    labelText: 'Keywords (comma-separated)',
                    hintText: 'e.g., AI, healthcare, innovation, technology',
                  ),
                ),

                const SizedBox(height: 16),

                // Word Count Slider
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        const Text('Number of words'),
                        Text(
                          '${_wordCount.toInt()} words',
                          style: const TextStyle(
                            color: AppTheme.primaryBlue,
                            fontWeight: FontWeight.w600,
                          ),
                        ),
                      ],
                    ),
                    const SizedBox(height: 8),
                    SliderTheme(
                      data: SliderTheme.of(context).copyWith(
                        activeTrackColor: AppTheme.primaryBlue,
                        thumbColor: AppTheme.primaryBlue,
                        overlayColor: AppTheme.primaryBlue.withOpacity(0.2),
                      ),
                      child: Slider(
                        value: _wordCount,
                        min: 200,
                        max: 2500,
                        divisions: 23,
                        onChanged: (value) {
                          setState(() {
                            _wordCount = value;
                          });
                        },
                      ),
                    ),
                  ],
                ),

                const SizedBox(height: 24),

                // Generate Button
                SizedBox(
                  width: double.infinity,
                  height: 50,
                  child: ElevatedButton(
                    onPressed: _isGenerating ? null : _generateBlog,
                    child: _isGenerating
                        ? Row(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              const SizedBox(
                                width: 20,
                                height: 20,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  valueColor: AlwaysStoppedAnimation<Color>(
                                      Colors.white),
                                ),
                              ),
                              const SizedBox(width: 12),
                              const Text('Generating...'),
                            ],
                          )
                        : const Text('Generate Blog'),
                  ),
                ),
              ],
            ),
          ),

          // Generated Blog Output
          if (_generatedBlog.isNotEmpty) ...[
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
                        'Generated Blog Post',
                        style: Theme.of(context).textTheme.titleLarge,
                      ),
                      ElevatedButton.icon(
                        onPressed: _copyToClipboard,
                        icon: const Icon(Icons.copy),
                        label: const Text('Copy'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: AppTheme.successColor,
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
                      data: _generatedBlog,
                      styleSheet: MarkdownStyleSheet(
                        p: const TextStyle(
                            color: AppTheme.textPrimary, height: 1.6),
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
                        em: const TextStyle(
                          color: AppTheme.primaryBlue,
                          fontStyle: FontStyle.italic,
                        ),
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
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }
}

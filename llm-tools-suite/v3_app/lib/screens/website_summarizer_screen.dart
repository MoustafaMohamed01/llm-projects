import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:flutter_markdown/flutter_markdown.dart';
import '../services/gemini_service.dart';
import '../theme/app_theme.dart';

class WebsiteSummarizerScreen extends StatefulWidget {
  const WebsiteSummarizerScreen({Key? key}) : super(key: key);

  @override
  State<WebsiteSummarizerScreen> createState() =>
      _WebsiteSummarizerScreenState();
}

class _WebsiteSummarizerScreenState extends State<WebsiteSummarizerScreen> {
  final TextEditingController _urlController = TextEditingController();
  final GeminiService _geminiService = GeminiService();

  bool _isProcessing = false;
  String _websiteTitle = '';
  String _extractedContent = '';
  String _summary = '';

  Future<void> _summarizeWebsite() async {
    final url = _urlController.text.trim();

    if (url.isEmpty) {
      _showSnackBar('Please enter a website URL.', AppTheme.warningColor);
      return;
    }

    if (!_isValidURL(url)) {
      _showSnackBar(
          'Please enter a valid URL starting with http:// or https://',
          AppTheme.errorColor);
      return;
    }

    setState(() {
      _isProcessing = true;
      _websiteTitle = '';
      _extractedContent = '';
      _summary = '';
    });

    try {
      // Attempt to fetch website content
      await _fetchWebsiteContent(url);

      if (_extractedContent.isNotEmpty) {
        await _generateSummary();
      } else {
        // Fallback: Generate summary based on URL analysis
        await _generateURLBasedSummary(url);
      }
    } catch (e) {
      setState(() {
        _isProcessing = false;
      });
      _showSnackBar(
          'Failed to process website. Please try again.', AppTheme.errorColor);
    }
  }

  Future<void> _fetchWebsiteContent(String url) async {
    try {
      // Note: This is a simplified approach. In production, you'd want a proper web scraping service
      final response = await http.get(
        Uri.parse(url),
        headers: {
          'User-Agent': 'Mozilla/5.0 (compatible; SummarizerBot/1.0)',
        },
      ).timeout(const Duration(seconds: 10));

      if (response.statusCode == 200) {
        String content = response.body;
        _extractWebsiteInfo(content, url);
      } else {
        throw Exception('Failed to fetch website: ${response.statusCode}');
      }
    } catch (e) {
      // If direct fetching fails, we'll use URL-based analysis
      print('Direct fetch failed: $e');
      _extractedContent = '';
    }
  }

  void _extractWebsiteInfo(String htmlContent, String url) {
    // Simple HTML parsing - extract title and basic content
    // This is a simplified approach; in production you'd use a proper HTML parser

    // Extract title
    RegExp titleRegex =
        RegExp(r'<title[^>]*>([^<]+)</title>', caseSensitive: false);
    Match? titleMatch = titleRegex.firstMatch(htmlContent);
    _websiteTitle = titleMatch?.group(1)?.trim() ?? 'Website';

    // Remove HTML tags and scripts (simplified)
    String cleanContent = htmlContent
        .replaceAll(
            RegExp(r'<script[^>]*>.*?</script>',
                caseSensitive: false, dotAll: true),
            '')
        .replaceAll(
            RegExp(r'<style[^>]*>.*?</style>',
                caseSensitive: false, dotAll: true),
            '')
        .replaceAll(RegExp(r'<[^>]+>'), ' ')
        .replaceAll(RegExp(r'\s+'), ' ')
        .trim();

    // Take a reasonable sample for analysis
    if (cleanContent.length > 5000) {
      _extractedContent = cleanContent.substring(0, 5000);
    } else {
      _extractedContent = cleanContent;
    }
  }

  Future<void> _generateSummary() async {
    final prompt =
        '''Please analyze and summarize the following website content:

Website Title: $_websiteTitle
URL: ${_urlController.text.trim()}

Content:
"""
$_extractedContent
"""

Provide a comprehensive summary that includes:
1. Main topic and purpose of the website
2. Key information and main points
3. Target audience or use case
4. Notable features or content highlights

Format the summary in clear, readable paragraphs.''';

    try {
      final summary = await _geminiService.generateResponse(prompt);
      setState(() {
        _summary = summary;
        _isProcessing = false;
      });
      _showSnackBar('Website summarized successfully!', AppTheme.successColor);
    } catch (e) {
      await _generateURLBasedSummary(_urlController.text.trim());
    }
  }

  Future<void> _generateURLBasedSummary(String url) async {
    final prompt =
        '''Based on the URL "$url", please provide an analysis of what this website likely contains and what kind of summary approach would be most effective.

Since direct content access is limited, please:
1. Analyze the domain and URL structure
2. Explain what type of website this appears to be
3. Suggest what kind of content analysis would be helpful
4. Provide guidance on how to effectively summarize this type of website

Note: This is a demonstration of website analysis capabilities. In a full implementation, this would include actual content scraping and detailed analysis.''';

    try {
      final analysis = await _geminiService.generateResponse(prompt);
      setState(() {
        _summary = analysis;
        _websiteTitle = 'Website Analysis';
        _isProcessing = false;
      });
      _showSnackBar('Website analysis completed!', AppTheme.successColor);
    } catch (e) {
      setState(() {
        _isProcessing = false;
      });
      throw e;
    }
  }

  bool _isValidURL(String url) {
    try {
      Uri.parse(url);
      return url.startsWith('http://') || url.startsWith('https://');
    } catch (e) {
      return false;
    }
  }

  void _copySummary() {
    if (_summary.isNotEmpty) {
      final fullContent = '''Website Summary: $_websiteTitle
URL: ${_urlController.text.trim()}

$_summary''';
      Clipboard.setData(ClipboardData(text: fullContent));
      _showSnackBar('Summary copied to clipboard!', AppTheme.successColor);
    }
  }

  void _clearSummary() {
    setState(() {
      _urlController.clear();
      _websiteTitle = '';
      _extractedContent = '';
      _summary = '';
    });
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
                        color: Colors.cyan.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Icon(
                        Icons.language,
                        color: Colors.cyan,
                        size: 32,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Website Summarizer',
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Summarize web pages by providing a URL.',
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

          // URL Input Form
          Container(
            padding: const EdgeInsets.all(24),
            decoration: AppTheme.cardGradient,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  'Website URL',
                  style: Theme.of(context).textTheme.titleLarge,
                ),
                const SizedBox(height: 4),
                Text(
                  'Enter the URL of the website you want to summarize',
                  style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                        color: AppTheme.textSecondary,
                      ),
                ),
                const SizedBox(height: 24),

                // URL Input
                TextField(
                  controller: _urlController,
                  decoration: const InputDecoration(
                    labelText: 'Website URL',
                    hintText: 'e.g., https://www.example.com',
                    prefixIcon: Icon(Icons.link),
                  ),
                  keyboardType: TextInputType.url,
                  textInputAction: TextInputAction.go,
                  onSubmitted: (_) => _summarizeWebsite(),
                ),

                const SizedBox(height: 16),

                // Info Card
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.blue.withOpacity(0.1),
                    borderRadius: BorderRadius.circular(8),
                    border: Border.all(color: Colors.blue.withOpacity(0.3)),
                  ),
                  child: Row(
                    children: [
                      Icon(Icons.info_outline, color: Colors.blue, size: 16),
                      const SizedBox(width: 8),
                      Expanded(
                        child: Text(
                          'Some websites may block automated access. The summarizer will adapt and provide URL-based analysis when needed.',
                          style: TextStyle(
                            color: Colors.blue,
                            fontSize: 12,
                          ),
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: 24),

                // Action Buttons
                Row(
                  children: [
                    Expanded(
                      child: OutlinedButton.icon(
                        onPressed: _urlController.text.isNotEmpty
                            ? _clearSummary
                            : null,
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
                        onPressed: _isProcessing ? null : _summarizeWebsite,
                        icon: _isProcessing
                            ? const SizedBox(
                                width: 16,
                                height: 16,
                                child: CircularProgressIndicator(
                                  strokeWidth: 2,
                                  valueColor: AlwaysStoppedAnimation<Color>(
                                      Colors.white),
                                ),
                              )
                            : const Icon(Icons.auto_awesome),
                        label: Text(_isProcessing
                            ? 'Processing...'
                            : 'Summarize Website'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.cyan,
                          padding: const EdgeInsets.symmetric(vertical: 12),
                        ),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),

          // Processing Indicator
          if (_isProcessing) ...[
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(16),
              decoration: AppTheme.cardGradient,
              child: Column(
                children: [
                  const CircularProgressIndicator(),
                  const SizedBox(height: 12),
                  Text(
                    'Fetching and analyzing website content...',
                    style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                          color: AppTheme.textSecondary,
                        ),
                  ),
                ],
              ),
            ),
          ],

          // Summary Output
          if (_summary.isNotEmpty) ...[
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
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Website Summary',
                              style: Theme.of(context).textTheme.titleLarge,
                            ),
                            if (_websiteTitle.isNotEmpty) ...[
                              const SizedBox(height: 4),
                              Text(
                                _websiteTitle,
                                style: Theme.of(context)
                                    .textTheme
                                    .titleMedium
                                    ?.copyWith(
                                      color: Colors.cyan,
                                    ),
                                maxLines: 2,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ],
                          ],
                        ),
                      ),
                      ElevatedButton.icon(
                        onPressed: _copySummary,
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
                      data: _summary,
                      styleSheet: MarkdownStyleSheet(
                        p: const TextStyle(
                          color: AppTheme.textPrimary,
                          height: 1.6,
                        ),
                        h1: const TextStyle(
                          color: AppTheme.primaryBlue,
                          fontWeight: FontWeight.bold,
                          fontSize: 20,
                        ),
                        h2: const TextStyle(
                          color: AppTheme.primaryBlue,
                          fontWeight: FontWeight.w600,
                          fontSize: 18,
                        ),
                        h3: const TextStyle(
                          color: AppTheme.primaryBlue,
                          fontWeight: FontWeight.w500,
                          fontSize: 16,
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

                  const SizedBox(height: 16),

                  // URL Reference
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.cyan.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.cyan.withOpacity(0.3)),
                    ),
                    child: Row(
                      children: [
                        Icon(Icons.link, color: Colors.cyan, size: 16),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            'Source: ${_urlController.text.trim()}',
                            style: TextStyle(
                              color: Colors.cyan,
                              fontSize: 12,
                              decoration: TextDecoration.underline,
                            ),
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                          ),
                        ),
                      ],
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
}

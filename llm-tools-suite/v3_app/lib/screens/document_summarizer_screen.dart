// lib/screens/document_summarizer_screen.dart
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import '../services/gemini_service.dart';
import '../services/document_processor.dart';
import '../theme/app_theme.dart';

class DocumentSummarizerScreen extends StatefulWidget {
  const DocumentSummarizerScreen({Key? key}) : super(key: key);

  @override
  State<DocumentSummarizerScreen> createState() =>
      _DocumentSummarizerScreenState();
}

class _DocumentSummarizerScreenState extends State<DocumentSummarizerScreen> {
  final GeminiService _geminiService = GeminiService();

  bool _isProcessing = false;
  String? _fileName;
  String _fileType = '';
  String _extractedText = '';
  String _summary = '';
  int _fileSize = 0;

  Future<void> _pickAndProcessDocument() async {
    try {
      // Show loading dialog
      showDialog(
        context: context,
        barrierDismissible: false,
        builder: (context) => const AlertDialog(
          content: Row(
            children: [
              CircularProgressIndicator(),
              SizedBox(width: 20),
              Text('Opening file picker...'),
            ],
          ),
        ),
      );

      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: DocumentProcessor.getSupportedExtensions(),
        allowMultiple: false,
        withData: true,
        allowCompression: false, // Important for PDF/DOCX files
      );

      // Close loading dialog
      if (mounted) Navigator.of(context).pop();

      if (result != null && result.files.isNotEmpty) {
        PlatformFile file = result.files.first;

        // Validate file type
        if (!DocumentProcessor.isSupportedFileType(file.name)) {
          _showSnackBar(
            'Unsupported file type. Please select PDF, Word, RTF, or text files.',
            AppTheme.warningColor,
          );
          return;
        }

        // Check file size (limit to 50MB for PDF/Word files)
        if (file.size > 50 * 1024 * 1024) {
          _showSnackBar(
            'File too large. Please select files smaller than 50MB.',
            AppTheme.warningColor,
          );
          return;
        }

        setState(() {
          _fileName = file.name;
          _fileSize = file.size;
          _fileType = DocumentProcessor.getFileTypeDescription(file.name);
          _isProcessing = true;
          _extractedText = '';
          _summary = '';
        });

        try {
          if (file.bytes != null) {
            await _processDocumentBytes(file.bytes!, file.name);
          } else {
            _showSnackBar('Could not read file content.', AppTheme.errorColor);
            _resetState();
          }
        } catch (e) {
          _showSnackBar('Error processing file: $e', AppTheme.errorColor);
          _resetState();
        }
      } else {
        _showSnackBar('No file selected.', AppTheme.warningColor);
      }
    } catch (e) {
      // Close loading dialog if still open
      if (mounted) {
        Navigator.of(context, rootNavigator: true)
            .popUntil((route) => route.isFirst);
      }
      _showSnackBar('Error accessing files: $e', AppTheme.errorColor);
    }
  }

  Future<void> _processDocumentBytes(
      Uint8List fileBytes, String fileName) async {
    try {
      // Show processing status
      _showSnackBar(
          'Extracting text from ${DocumentProcessor.getFileTypeDescription(fileName)}...',
          AppTheme.primaryBlue);

      // Extract text using the document processor
      String extractedText =
          await DocumentProcessor.processDocument(fileBytes, fileName);

      if (extractedText.trim().isEmpty) {
        _showSnackBar(
            'No readable text found in the document.', AppTheme.warningColor);
        _resetState();
        return;
      }

      setState(() {
        _extractedText = extractedText;
      });

      // Show text extraction success
      _showSnackBar('Text extracted successfully! Generating summary...',
          AppTheme.successColor);

      // Generate summary
      await _generateSummary(extractedText);
    } catch (e) {
      _showSnackBar('Error processing document: $e', AppTheme.errorColor);
      _resetState();
    }
  }

  Future<void> _generateSummary(String content) async {
    try {
      // Prepare content for processing
      String processContent = content.trim();

      // For very large documents, take a reasonable sample
      if (processContent.length > 20000) {
        // Take beginning, middle, and end sections
        String beginning = processContent.substring(0, 7000);
        int middle = processContent.length ~/ 2;
        String middleSection =
            processContent.substring(middle - 3000, middle + 3000);
        String ending = processContent.substring(processContent.length - 7000);

        processContent =
            '$beginning\n\n[... middle section ...]\n\n$middleSection\n\n[... end section ...]\n\n$ending';
        _showSnackBar('Large document processed with sampling technique.',
            AppTheme.warningColor);
      }

      final prompt =
          '''Please provide a comprehensive summary of the following document. This is a ${_fileType} file named "$_fileName".

Please structure your summary with:

## Document Overview
- **Type**: ${_fileType}
- **Main Subject**: What is this document primarily about?
- **Purpose**: Why was this document created?

## Key Content Analysis
1. **Main Topics**: The primary themes and subjects covered
2. **Important Points**: Critical information, findings, or arguments
3. **Structure**: How the content is organized
4. **Key Data/Facts**: Any important statistics, dates, or specific information

## Conclusions & Takeaways
- **Main Conclusions**: What does the document conclude?
- **Actionable Insights**: What should readers know or do?
- **Significance**: Why is this document important?

---

**Document Content:**
```
$processContent
```

Please provide a well-structured, comprehensive summary that captures the essence and value of this document.''';

      final summary = await _geminiService.generateResponse(prompt);

      setState(() {
        _summary = summary;
        _isProcessing = false;
      });

      _showSnackBar('Document summarized successfully!', AppTheme.successColor);
    } catch (e) {
      setState(() {
        _isProcessing = false;
      });
      _showSnackBar('Failed to generate summary: $e', AppTheme.errorColor);
    }
  }

  void _resetState() {
    setState(() {
      _fileName = null;
      _fileType = '';
      _extractedText = '';
      _summary = '';
      _fileSize = 0;
      _isProcessing = false;
    });
  }

  void _copySummary() {
    if (_summary.isNotEmpty) {
      final fullContent = '''Document Summary: $_fileName
File Type: $_fileType
Original Size: ${_formatFileSize(_fileSize)}
Text Length: ${_extractedText.length} characters

$_summary

---
Generated by LLM Tools Suite''';

      Clipboard.setData(ClipboardData(text: fullContent));
      _showSnackBar('Summary copied to clipboard!', AppTheme.successColor);
    }
  }

  void _clearDocument() {
    _resetState();
  }

  String _formatFileSize(int bytes) {
    if (bytes < 1024) return '$bytes B';
    if (bytes < 1024 * 1024) return '${(bytes / 1024).toStringAsFixed(1)} KB';
    return '${(bytes / (1024 * 1024)).toStringAsFixed(1)} MB';
  }

  void _showSnackBar(String message, Color color) {
    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(message),
          backgroundColor: color,
          duration: const Duration(seconds: 4),
          behavior: SnackBarBehavior.floating,
        ),
      );
    }
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
                        color: Colors.red.withOpacity(0.2),
                        borderRadius: BorderRadius.circular(12),
                      ),
                      child: const Icon(
                        Icons.description,
                        color: Colors.red,
                        size: 32,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Document Summarizer',
                            style: Theme.of(context).textTheme.headlineSmall,
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Upload PDF, Word, and text documents for AI-powered analysis.',
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

          // File Upload Section
          if (_fileName == null) ...[
            Container(
              padding: const EdgeInsets.all(32),
              decoration: AppTheme.cardGradient,
              child: Column(
                children: [
                  Container(
                    padding: const EdgeInsets.all(24),
                    decoration: BoxDecoration(
                      color: Colors.red.withOpacity(0.1),
                      borderRadius: BorderRadius.circular(16),
                      border: Border.all(
                        color: Colors.red.withOpacity(0.3),
                        width: 2,
                        style: BorderStyle.solid,
                      ),
                    ),
                    child: Column(
                      children: [
                        Icon(
                          Icons.upload_file,
                          size: 48,
                          color: Colors.red.withOpacity(0.7),
                        ),
                        const SizedBox(height: 16),
                        Text(
                          'Upload Document',
                          style:
                              Theme.of(context).textTheme.titleLarge?.copyWith(
                                    color: Colors.red,
                                  ),
                        ),
                        const SizedBox(height: 12),

                        // Supported formats grid
                        Wrap(
                          alignment: WrapAlignment.center,
                          spacing: 8,
                          runSpacing: 8,
                          children: [
                            _buildFileTypeChip(
                                'PDF', Icons.picture_as_pdf, Colors.red),
                            _buildFileTypeChip(
                                'DOCX', Icons.description, Colors.blue),
                            _buildFileTypeChip(
                                'DOC', Icons.description_outlined, Colors.blue),
                            _buildFileTypeChip(
                                'RTF', Icons.text_snippet, Colors.orange),
                            _buildFileTypeChip(
                                'TXT', Icons.text_fields, Colors.green),
                            _buildFileTypeChip('MD', Icons.code, Colors.purple),
                            _buildFileTypeChip(
                                'CSV', Icons.table_chart, Colors.teal),
                          ],
                        ),

                        const SizedBox(height: 16),
                        Text(
                          'Maximum file size: 50MB',
                          style:
                              Theme.of(context).textTheme.bodySmall?.copyWith(
                                    color: AppTheme.textSecondary,
                                  ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: 24),
                  ElevatedButton.icon(
                    onPressed: _pickAndProcessDocument,
                    icon: const Icon(Icons.folder_open),
                    label: const Text('Select Document'),
                    style: ElevatedButton.styleFrom(
                      backgroundColor: Colors.red,
                      padding: const EdgeInsets.symmetric(
                        horizontal: 32,
                        vertical: 16,
                      ),
                    ),
                  ),
                  const SizedBox(height: 12),
                  TextButton(
                    onPressed: () {
                      showDialog(
                        context: context,
                        builder: (context) => AlertDialog(
                          title: const Text('Supported File Types'),
                          content: const Text(
                            'PDF Documents (.pdf)\n'
                            '• Extracts text from all pages\n'
                            '• Handles formatted documents\n\n'
                            'Word Documents (.docx, .doc)\n'
                            '• Microsoft Word files\n'
                            '• Text formatting preserved\n\n'
                            'Text Files (.txt, .md, .rtf, .csv)\n'
                            '• Plain text and formatted text\n'
                            '• Markdown and rich text\n\n'
                            'Note: Scanned documents (images) may not extract text properly.',
                          ),
                          actions: [
                            TextButton(
                              onPressed: () => Navigator.of(context).pop(),
                              child: const Text('Got it'),
                            ),
                          ],
                        ),
                      );
                    },
                    child: const Text('Supported file types'),
                  ),
                ],
              ),
            ),
          ] else ...[
            // Document Processing/Results
            Container(
              padding: const EdgeInsets.all(16),
              decoration: AppTheme.cardGradient,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(8),
                        decoration: BoxDecoration(
                          color: Colors.red.withOpacity(0.2),
                          borderRadius: BorderRadius.circular(8),
                        ),
                        child: Icon(_getFileIcon(_fileName!),
                            color: Colors.red, size: 20),
                      ),
                      const SizedBox(width: 12),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              _fileName!,
                              style: Theme.of(context).textTheme.titleMedium,
                              maxLines: 2,
                              overflow: TextOverflow.ellipsis,
                            ),
                            Text(
                              '$_fileType • ${_formatFileSize(_fileSize)} • ${_extractedText.length} characters',
                              style: Theme.of(context)
                                  .textTheme
                                  .bodySmall
                                  ?.copyWith(
                                    color: AppTheme.textSecondary,
                                  ),
                            ),
                          ],
                        ),
                      ),
                      TextButton.icon(
                        onPressed: _clearDocument,
                        icon: const Icon(Icons.refresh),
                        label: const Text('New File'),
                      ),
                    ],
                  ),
                  if (_isProcessing) ...[
                    const SizedBox(height: 16),
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: Colors.orange.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(8),
                        border:
                            Border.all(color: Colors.orange.withOpacity(0.3)),
                      ),
                      child: Column(
                        children: [
                          const CircularProgressIndicator(),
                          const SizedBox(height: 12),
                          Text(
                            'Processing ${_fileType}...',
                            style: Theme.of(context).textTheme.titleMedium,
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Extracting text and generating comprehensive summary',
                            style:
                                Theme.of(context).textTheme.bodySmall?.copyWith(
                                      color: AppTheme.textSecondary,
                                    ),
                            textAlign: TextAlign.center,
                          ),
                        ],
                      ),
                    ),
                  ],
                ],
              ),
            ),

            // Document Preview (when text is extracted but processing)
            if (_extractedText.isNotEmpty &&
                !_isProcessing &&
                _summary.isEmpty) ...[
              const SizedBox(height: 16),
              Container(
                padding: const EdgeInsets.all(16),
                decoration: AppTheme.cardGradient,
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      'Extracted Text Preview',
                      style: Theme.of(context).textTheme.titleMedium,
                    ),
                    const SizedBox(height: 12),
                    Container(
                      height: 200,
                      padding: const EdgeInsets.all(12),
                      decoration: BoxDecoration(
                        color: Colors.white.withOpacity(0.05),
                        borderRadius: BorderRadius.circular(8),
                        border:
                            Border.all(color: Colors.white.withOpacity(0.1)),
                      ),
                      child: SingleChildScrollView(
                        child: Text(
                          _extractedText.length > 1000
                              ? '${_extractedText.substring(0, 1000)}...'
                              : _extractedText,
                          style:
                              Theme.of(context).textTheme.bodySmall?.copyWith(
                                    height: 1.4,
                                  ),
                        ),
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
                          child: Text(
                            'Document Analysis & Summary',
                            style: Theme.of(context).textTheme.titleLarge,
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
                              color: AppTheme.textPrimary, height: 1.6),
                          h1: const TextStyle(
                            color: AppTheme.primaryBlue,
                            fontWeight: FontWeight.bold,
                            fontSize: 22,
                          ),
                          h2: const TextStyle(
                            color: AppTheme.primaryBlue,
                            fontWeight: FontWeight.w600,
                            fontSize: 18,
                          ),
                          h3: const TextStyle(
                            color: AppTheme.secondaryBlue,
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
                  ],
                ),
              ),
            ],
          ],

          const SizedBox(height: 16),
        ],
      ),
    );
  }

  Widget _buildFileTypeChip(String label, IconData icon, Color color) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: color.withOpacity(0.3)),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, color: color, size: 14),
          const SizedBox(width: 4),
          Text(
            label,
            style: TextStyle(
              color: color,
              fontSize: 12,
              fontWeight: FontWeight.w600,
            ),
          ),
        ],
      ),
    );
  }

  IconData _getFileIcon(String fileName) {
    String extension = fileName.toLowerCase().split('.').last;
    switch (extension) {
      case 'pdf':
        return Icons.picture_as_pdf;
      case 'docx':
      case 'doc':
        return Icons.description;
      case 'rtf':
        return Icons.text_snippet;
      case 'txt':
        return Icons.text_fields;
      case 'md':
        return Icons.code;
      case 'csv':
        return Icons.table_chart;
      default:
        return Icons.insert_drive_file;
    }
  }
}

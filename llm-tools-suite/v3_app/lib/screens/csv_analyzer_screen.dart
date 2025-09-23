import 'package:flutter/material.dart';
import 'package:file_picker/file_picker.dart';
import 'package:csv/csv.dart';
import 'dart:io';
import '../models/tool_model.dart';
import '../services/chat_service.dart';
import '../services/gemini_service.dart';
import '../theme/app_theme.dart';
import '../widgets/loading_animation.dart';

class CSVAnalyzerScreen extends StatefulWidget {
  const CSVAnalyzerScreen({Key? key}) : super(key: key);

  @override
  State<CSVAnalyzerScreen> createState() => _CSVAnalyzerScreenState();
}

class _CSVAnalyzerScreenState extends State<CSVAnalyzerScreen> {
  final TextEditingController _questionController = TextEditingController();
  final ScrollController _scrollController = ScrollController();
  final ChatService _chatService = ChatService();
  final GeminiService _geminiService = GeminiService();

  List<ChatMessage> _messages = [];
  bool _isLoading = false;
  String? _fileName;
  List<List<String>> _csvData = [];
  List<String> _headers = [];
  static const String _toolId = 'csv-analyzer';

  @override
  void initState() {
    super.initState();
    _loadChatHistory();
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

  Future<void> _pickAndUploadFile() async {
    try {
      FilePickerResult? result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['csv'],
        allowMultiple: false,
        withData: true,
      );

      if (result != null) {
        PlatformFile file = result.files.first;

        if (file.bytes != null) {
          String csvString = String.fromCharCodes(file.bytes!);
          await _processCsvData(csvString, file.name);
        } else if (file.path != null) {
          File csvFile = File(file.path!);
          String csvString = await csvFile.readAsString();
          await _processCsvData(csvString, file.name);
        }
      }
    } catch (e) {
      _showSnackBar('Error loading CSV file: $e', AppTheme.errorColor);
    }
  }

  Future<void> _processCsvData(String csvString, String fileName) async {
    try {
      List<List<dynamic>> csvTable =
          const CsvToListConverter().convert(csvString);

      if (csvTable.isEmpty) {
        _showSnackBar('CSV file is empty', AppTheme.warningColor);
        return;
      }

      setState(() {
        _fileName = fileName;
        _csvData = csvTable
            .map((row) => row.map((cell) => cell.toString()).toList())
            .toList();
        _headers = _csvData.isNotEmpty ? _csvData[0] : [];
      });

      _showSnackBar(
          'CSV uploaded successfully! ${_csvData.length - 1} rows, ${_headers.length} columns.',
          AppTheme.successColor);
    } catch (e) {
      _showSnackBar('Error parsing CSV: $e', AppTheme.errorColor);
    }
  }

  Future<void> _askQuestion() async {
    final question = _questionController.text.trim();
    if (question.isEmpty || _csvData.isEmpty || _isLoading) return;

    // Add user message
    final userMessage = ChatMessage(
      content: question,
      isUser: true,
      timestamp: DateTime.now(),
      toolId: _toolId,
    );

    setState(() {
      _messages.add(userMessage);
      _isLoading = true;
    });

    _questionController.clear();
    _scrollToBottom();

    try {
      // Prepare CSV sample for analysis
      String csvSample = _prepareCsvSample();

      final prompt =
          '''You are an expert data analysis assistant. The user has provided a CSV dataset with the following columns: ${_headers.join(', ')}.

Here is a sample of the CSV data:
```csv
${csvSample}
```

Dataset summary: ${_csvData.length - 1} rows, ${_headers.length} columns.

Please answer the following question about the data professionally and provide actionable insights if applicable:

Question: $question''';

      final response = await _geminiService.generateResponse(prompt);

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
          content: "Error analyzing data: ${e.toString()}",
          isUser: false,
          timestamp: DateTime.now(),
          toolId: _toolId,
        ));
      });
    }

    _scrollToBottom();
  }

  String _prepareCsvSample() {
    if (_csvData.isEmpty) return '';

    // Include headers and first 10 rows for analysis
    List<List<String>> sample = _csvData.take(11).toList();
    return sample.map((row) => row.join(',')).join('\n');
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
    return Column(
      children: [
        // Header
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
                      color: Colors.green.withOpacity(0.2),
                      borderRadius: BorderRadius.circular(12),
                    ),
                    child: const Icon(
                      Icons.analytics,
                      color: Colors.green,
                      size: 32,
                    ),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'AI CSV Analyzer',
                          style: Theme.of(context).textTheme.headlineSmall,
                        ),
                        const SizedBox(height: 4),
                        Text(
                          'Upload and analyze your CSV data using AI.',
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

        // File Upload Section
        if (_csvData.isEmpty) ...[
          Expanded(
            child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 16),
              decoration: AppTheme.cardGradient,
              child: Center(
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Container(
                      padding: const EdgeInsets.all(32),
                      decoration: BoxDecoration(
                        color: Colors.green.withOpacity(0.1),
                        borderRadius: BorderRadius.circular(20),
                        border: Border.all(
                          color: Colors.green.withOpacity(0.3),
                          width: 2,
                          style: BorderStyle.solid,
                        ),
                      ),
                      child: Column(
                        children: [
                          Icon(
                            Icons.upload_file,
                            size: 64,
                            color: Colors.green.withOpacity(0.7),
                          ),
                          const SizedBox(height: 16),
                          Text(
                            'Upload CSV File',
                            style: Theme.of(context)
                                .textTheme
                                .titleLarge
                                ?.copyWith(
                                  color: Colors.green,
                                ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Click to select a CSV file from your device',
                            style: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.copyWith(
                                  color: AppTheme.textSecondary,
                                ),
                            textAlign: TextAlign.center,
                          ),
                          const SizedBox(height: 24),
                          ElevatedButton.icon(
                            onPressed: _pickAndUploadFile,
                            icon: const Icon(Icons.folder_open),
                            label: const Text('Select CSV File'),
                            style: ElevatedButton.styleFrom(
                              backgroundColor: Colors.green,
                              padding: const EdgeInsets.symmetric(
                                horizontal: 32,
                                vertical: 16,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),
            ),
          ),
        ] else ...[
          // Data Preview
          Container(
            margin: const EdgeInsets.symmetric(horizontal: 16),
            padding: const EdgeInsets.all(16),
            decoration: AppTheme.cardGradient,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Data Preview: $_fileName',
                            style: Theme.of(context).textTheme.titleMedium,
                          ),
                          Text(
                            '${_csvData.length - 1} rows, ${_headers.length} columns',
                            style:
                                Theme.of(context).textTheme.bodySmall?.copyWith(
                                      color: AppTheme.textSecondary,
                                    ),
                          ),
                        ],
                      ),
                    ),
                    TextButton.icon(
                      onPressed: () {
                        setState(() {
                          _csvData = [];
                          _headers = [];
                          _fileName = null;
                          _messages = [];
                        });
                      },
                      icon: const Icon(Icons.refresh),
                      label: const Text('Upload New'),
                    ),
                  ],
                ),
                const SizedBox(height: 16),
                if (_headers.isNotEmpty)
                  Container(
                    height: 200,
                    decoration: BoxDecoration(
                      border: Border.all(color: Colors.white.withOpacity(0.2)),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: SingleChildScrollView(
                      scrollDirection: Axis.vertical,
                      child: DataTable(
                        headingRowColor: MaterialStateColor.resolveWith(
                          (states) => Colors.green.withOpacity(0.2),
                        ),
                        columns: _headers
                            .map((header) => DataColumn(
                                  label: Text(
                                    header,
                                    style: const TextStyle(
                                        fontWeight: FontWeight.bold),
                                  ),
                                ))
                            .toList(),
                        rows: _csvData
                            .skip(1)
                            .take(5)
                            .map((row) => DataRow(
                                  cells: row
                                      .map((cell) => DataCell(
                                            Text(cell,
                                                style: const TextStyle(
                                                    fontSize: 12)),
                                          ))
                                      .toList(),
                                ))
                            .toList(),
                      ),
                    ),
                  ),
              ],
            ),
          ),

          const SizedBox(height: 16),

          // Chat Section
          Expanded(
            child: Container(
              margin: const EdgeInsets.symmetric(horizontal: 16),
              decoration: AppTheme.cardGradient,
              child: Column(
                children: [
                  // Chat Messages
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

                  // Input Area
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
                            controller: _questionController,
                            decoration: const InputDecoration(
                              hintText: 'Ask a question about your data...',
                              border: OutlineInputBorder(),
                            ),
                            maxLines: null,
                            textInputAction: TextInputAction.send,
                            onSubmitted: (_) => _askQuestion(),
                          ),
                        ),
                        const SizedBox(width: 12),
                        ElevatedButton(
                          onPressed: _isLoading ? null : _askQuestion,
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
                              : const Text('Ask'),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],

        const SizedBox(height: 16),
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
                color: Colors.green.withOpacity(0.2),
                borderRadius: BorderRadius.circular(20),
              ),
              child: const Icon(
                Icons.analytics,
                color: Colors.green,
                size: 16,
              ),
            ),
            const SizedBox(width: 12),
          ],
          Expanded(
            child: Container(
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
              child: Text(
                message.content,
                style: TextStyle(
                  color: message.isUser ? Colors.white : AppTheme.textPrimary,
                ),
              ),
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
}

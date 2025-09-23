import 'package:flutter/material.dart';
import '../services/gemini_service.dart';
import '../theme/app_theme.dart';

class SQLGeneratorScreen extends StatefulWidget {
  const SQLGeneratorScreen({Key? key}) : super(key: key);

  @override
  State<SQLGeneratorScreen> createState() => _SQLGeneratorScreenState();
}

class _SQLGeneratorScreenState extends State<SQLGeneratorScreen> {
  final TextEditingController _descriptionController = TextEditingController();
  final TextEditingController _contextController = TextEditingController();
  final GeminiService _geminiService = GeminiService();

  String _selectedDialect = 'Generic SQL';
  bool _isGenerating = false;
  String _generatedSQL = '';
  String _explanation = '';

  final List<String> _dialects = [
    'Generic SQL',
    'PostgreSQL',
    'MySQL',
    'SQLite',
    'SQL Server',
    'Oracle'
  ];

  Future<void> _generateSQL() async {
    if (_descriptionController.text.trim().isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Please provide a query description.')),
      );
      return;
    }

    setState(() {
      _isGenerating = true;
    });

    try {
      final sqlPrompt =
          '''Generate a $_selectedDialect SQL query based on the following description:
Description: ${_descriptionController.text.trim()}
${_contextController.text.trim().isNotEmpty ? 'Database Context: ${_contextController.text.trim()}' : ''}
Provide only the SQL query as a raw string, without any additional explanations or formatting.''';

      final sql = await _geminiService.generateResponse(sqlPrompt);

      final explanationPrompt = '''Explain the following SQL Query concisely:
```sql
$sql
```
Focus on what the query does and its purpose.''';

      final explanation =
          await _geminiService.generateResponse(explanationPrompt);

      setState(() {
        _generatedSQL = sql;
        _explanation = explanation;
        _isGenerating = false;
      });
    } catch (e) {
      setState(() {
        _isGenerating = false;
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Error: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        children: [
          // Header
          Container(
            padding: const EdgeInsets.all(24),
            decoration: AppTheme.cardGradient,
            child: Row(
              children: [
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: Colors.purple.withOpacity(0.2),
                    borderRadius: BorderRadius.circular(12),
                  ),
                  child: const Icon(Icons.code, color: Colors.purple, size: 32),
                ),
                const SizedBox(width: 16),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text('SQL Query Generator',
                          style: Theme.of(context).textTheme.headlineSmall),
                      Text(
                          'Generate SQL queries from natural language descriptions.',
                          style: Theme.of(context)
                              .textTheme
                              .bodyMedium
                              ?.copyWith(color: AppTheme.textSecondary)),
                    ],
                  ),
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
              children: [
                TextField(
                  controller: _descriptionController,
                  decoration:
                      const InputDecoration(labelText: 'Query Description'),
                  maxLines: 3,
                ),
                const SizedBox(height: 16),
                TextField(
                  controller: _contextController,
                  decoration: const InputDecoration(
                      labelText: 'Database Context (Optional)'),
                  maxLines: 2,
                ),
                const SizedBox(height: 16),
                DropdownButtonFormField<String>(
                  value: _selectedDialect,
                  decoration: const InputDecoration(labelText: 'SQL Dialect'),
                  items: _dialects
                      .map((dialect) => DropdownMenuItem(
                          value: dialect, child: Text(dialect)))
                      .toList(),
                  onChanged: (value) =>
                      setState(() => _selectedDialect = value!),
                ),
                const SizedBox(height: 24),
                SizedBox(
                  width: double.infinity,
                  child: ElevatedButton(
                    onPressed: _isGenerating ? null : _generateSQL,
                    child: _isGenerating
                        ? const CircularProgressIndicator()
                        : const Text('Generate SQL Query'),
                  ),
                ),
              ],
            ),
          ),
          if (_generatedSQL.isNotEmpty) ...[
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(24),
              decoration: AppTheme.cardGradient,
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text('Generated SQL Query:',
                      style: Theme.of(context).textTheme.titleLarge),
                  const SizedBox(height: 16),
                  Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: Colors.black.withOpacity(0.3),
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: SelectableText(_generatedSQL,
                        style: const TextStyle(fontFamily: 'monospace')),
                  ),
                  const SizedBox(height: 16),
                  Text('Explanation:',
                      style: Theme.of(context).textTheme.titleMedium),
                  const SizedBox(height: 8),
                  Text(_explanation),
                ],
              ),
            ),
          ],
        ],
      ),
    );
  }
}

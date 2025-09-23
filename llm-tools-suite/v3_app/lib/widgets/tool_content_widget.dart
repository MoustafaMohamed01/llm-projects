import 'package:flutter/material.dart';
import '../models/tool_model.dart';
import '../screens/ai_assistant_screen.dart';
import '../screens/blog_assistant_screen.dart';
import '../screens/csv_analyzer_screen.dart';
import '../screens/sql_generator_screen.dart';
import '../screens/document_summarizer_screen.dart';
import '../screens/website_summarizer_screen.dart';
import '../screens/code_explainer_screen.dart';

class ToolContentWidget extends StatelessWidget {
  final ToolModel tool;

  const ToolContentWidget({
    Key? key,
    required this.tool,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    switch (tool.id) {
      case 'ai-assistant':
        return const AIAssistantScreen();
      case 'blog-assistant':
        return const BlogAssistantScreen();
      case 'csv-analyzer':
        return const CSVAnalyzerScreen();
      case 'sql-generator':
        return const SQLGeneratorScreen();
      case 'document-summarizer':
        return const DocumentSummarizerScreen();
      case 'website-summarizer':
        return const WebsiteSummarizerScreen();
      case 'code-explainer':
        return const CodeExplainerScreen();
      default:
        return const Center(
          child: Text('Tool not found'),
        );
    }
  }
}

import 'package:flutter/material.dart';
import '../models/tool_model.dart';
import '../widgets/sidebar_widget.dart';
import '../widgets/tool_content_widget.dart';
import '../theme/app_theme.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int selectedToolIndex = 0;
  bool isSidebarOpen = true;

  final List<ToolModel> tools = [
    ToolModel(
      id: 'ai-assistant',
      name: 'AI Assistant',
      icon: Icons.psychology,
      description: 'Chat with a professional AI assistant',
      color: AppTheme.primaryBlue,
    ),
    ToolModel(
      id: 'blog-assistant',
      name: 'Blog AI Assistant',
      icon: Icons.article,
      description: 'Generate engaging blog posts with AI assistance',
      color: Colors.orange,
    ),
    ToolModel(
      id: 'csv-analyzer',
      name: 'AI CSV Analyzer',
      icon: Icons.analytics,
      description: 'Upload and analyze your CSV data using AI',
      color: Colors.green,
    ),
    ToolModel(
      id: 'sql-generator',
      name: 'SQL Query Generator',
      icon: Icons.code,
      description: 'Generate SQL queries from natural language descriptions',
      color: Colors.purple,
    ),
    ToolModel(
      id: 'document-summarizer',
      name: 'Document Summarizer',
      icon: Icons.description,
      description: 'Summarize PDF and Word documents instantly',
      color: Colors.red,
    ),
    ToolModel(
      id: 'website-summarizer',
      name: 'Website Summarizer',
      icon: Icons.language,
      description: 'Summarize web pages by providing a URL',
      color: Colors.cyan,
    ),
    ToolModel(
      id: 'code-explainer',
      name: 'Code Explainer',
      icon: Icons.integration_instructions,
      description: 'Understand code with AI-powered step-by-step explanations',
      color: Colors.indigo,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Container(
        decoration: AppTheme.backgroundGradient,
        child: Row(
          children: [
            // Sidebar
            if (isSidebarOpen || MediaQuery.of(context).size.width > 768)
              SidebarWidget(
                tools: tools,
                selectedIndex: selectedToolIndex,
                onToolSelected: (index) {
                  setState(() {
                    selectedToolIndex = index;
                    if (MediaQuery.of(context).size.width <= 768) {
                      isSidebarOpen = false;
                    }
                  });
                },
                onToggleSidebar: () {
                  setState(() {
                    isSidebarOpen = !isSidebarOpen;
                  });
                },
              ),

            // Main Content
            Expanded(
              child: Column(
                children: [
                  // Top App Bar
                  if (!isSidebarOpen ||
                      MediaQuery.of(context).size.width <= 768)
                    Container(
                      padding: const EdgeInsets.all(16),
                      decoration: BoxDecoration(
                        color: AppTheme.darkSecondary.withOpacity(0.8),
                        border: Border(
                          bottom: BorderSide(
                            color: Colors.white.withOpacity(0.1),
                          ),
                        ),
                      ),
                      child: Row(
                        children: [
                          IconButton(
                            icon: const Icon(Icons.menu),
                            onPressed: () {
                              setState(() {
                                isSidebarOpen = !isSidebarOpen;
                              });
                            },
                          ),
                          const SizedBox(width: 16),
                          Text(
                            tools[selectedToolIndex].name,
                            style: Theme.of(context).textTheme.titleLarge,
                          ),
                        ],
                      ),
                    ),

                  // Tool Content
                  Expanded(
                    child: ToolContentWidget(
                      tool: tools[selectedToolIndex],
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

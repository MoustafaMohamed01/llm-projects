import 'package:flutter/material.dart';
import '../theme/app_theme.dart';

class LoadingAnimation extends StatefulWidget {
  const LoadingAnimation({Key? key}) : super(key: key);

  @override
  State<LoadingAnimation> createState() => _LoadingAnimationState();
}

class _LoadingAnimationState extends State<LoadingAnimation>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    )..repeat();

    _animation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeInOut,
    ));
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
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
        Container(
          padding: const EdgeInsets.all(16),
          decoration: BoxDecoration(
            color: Colors.white.withOpacity(0.1),
            borderRadius: BorderRadius.circular(16),
            border: Border.all(color: Colors.white.withOpacity(0.1)),
          ),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text('AI is thinking'),
              const SizedBox(width: 8),
              AnimatedBuilder(
                animation: _animation,
                builder: (context, child) {
                  return Row(
                    children: List.generate(3, (index) {
                      final delay = index * 0.2;
                      final animValue =
                          (_animation.value - delay).clamp(0.0, 1.0);
                      final opacity =
                          (1.0 - (animValue - 0.5).abs() * 2).clamp(0.3, 1.0);

                      return Container(
                        margin: const EdgeInsets.symmetric(horizontal: 2),
                        child: Opacity(
                          opacity: opacity,
                          child: const Text(
                            '●',
                            style: TextStyle(
                              color: AppTheme.primaryBlue,
                              fontSize: 16,
                            ),
                          ),
                        ),
                      );
                    }),
                  );
                },
              ),
            ],
          ),
        ),
      ],
    );
  }
}

<svelte:head>
  <title>ふうりん - Japanese Learning Platform</title>
</svelte:head>

<!-- Paste main HTML from index.html body minus <html>,<head>,<body> -->
<!-- We keep asset paths as absolute from project root -->

<!-- Top Navigation -->
<header class="top-nav">
    <div class="top-nav-content">
        <div>
            <h1 class="logo">ふうりん</h1>
        </div>
        <div class="nav-buttons">
            <button class="nav-button">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M6 8a6 6 0 0 1 12 0c0 7 3 9 3 9H3s3-2 3-9"/>
                    <path d="M10.3 21a1.94 1.94 0 0 0 3.4 0"/>
                </svg>
                <span class="notification-dot"></span>
            </button>
            <button class="nav-button">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
                    <circle cx="12" cy="7" r="4"/>
                </svg>
            </button>
        </div>
    </div>
</header>

<!-- Sidebar Navigation -->
<div class="sidebar">
    <div class="sidebar-content">
        <div class="sidebar-header">
            <h2 class="sidebar-title">ナビゲーション</h2>
            <p class="sidebar-subtitle">Navigate your learning journey</p>
        </div>

        <nav class="nav-items">
            <a href="/" class="nav-item active">
                <div class="nav-icon">家</div>
                <div class="nav-text">
                    <div class="nav-name">Home</div>
                    <div class="nav-desc">Dashboard</div>
                </div>
                <div class="active-indicator"></div>
            </a>
            <a href="/dashboard" class="nav-item">
                <div class="nav-icon">板</div>
                <div class="nav-text">
                    <div class="nav-name">Dashboard</div>
                    <div class="nav-desc">Overview</div>
                </div>
            </a>
            <a href="#" class="nav-item">
                <div class="nav-icon">賞</div>
                <div class="nav-text">
                    <div class="nav-name">Awards</div>
                    <div class="nav-desc">Achievements</div>
                </div>
            </a>
            <a href="/activity-feed" class="nav-item">
                <div class="nav-icon">活</div>
                <div class="nav-text">
                    <div class="nav-name">Feed</div>
                    <div class="nav-desc">Recent</div>
                </div>
            </a>
            <a href="#" class="nav-item">
                <div class="nav-icon">順</div>
                <div class="nav-text">
                    <div class="nav-name">Leaderboard</div>
                    <div class="nav-desc">Rankings</div>
                </div>
            </a>
            <a href="#" class="nav-item">
                <div class="nav-icon">図</div>
                <div class="nav-text">
                    <div class="nav-name">Library</div>
                    <div class="nav-desc">Resources</div>
                </div>
            </a>
            <a href="#" class="nav-item">
                <div class="nav-icon">統</div>
                <div class="nav-text">
                    <div class="nav-name">Stats</div>
                    <div class="nav-desc">Analytics</div>
                </div>
            </a>
            <a href="#" class="nav-item">
                <div class="nav-icon">購</div>
                <div class="nav-text">
                    <div class="nav-name">Subscribe</div>
                    <div class="nav-desc">Premium</div>
                </div>
            </a>
            <a href="#" class="nav-item">
                <div class="nav-icon">投</div>
                <div class="nav-text">
                    <div class="nav-name">Submit</div>
                    <div class="nav-desc">Upload</div>
                </div>
            </a>
            <a href="#" class="nav-item">
                <div class="nav-icon">人</div>
                <div class="nav-text">
                    <div class="nav-name">Profile</div>
                    <div class="nav-desc">Settings</div>
                </div>
            </a>
        </nav>

        <div class="study-streak">
            <div class="streak-content">
                <div class="streak-icon">学</div>
                <div>
                    <div class="streak-text">Study Streak</div>
                    <div class="streak-subtext">23 days strong!</div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Main Content -->
<main class="main-content" id="content">
    <div class="content-wrapper">
        <!-- Welcome Section -->
        <div class="welcome-section">
            <h1 class="welcome-title">おかえりなさい！</h1>
            <h2 class="welcome-subtitle">Welcome back to your Japanese journey</h2>
            <p class="welcome-description">
                Continue your path to fluency with ふうりん. Track your progress and discover new learning opportunities.
            </p>
            <button class="continue-button">Continue Learning</button>
        </div>

        <!-- Stats Cards -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-header">
                    <div class="stat-title">Words Learned</div>
                    <div class="stat-icon">語</div>
                </div>
                <div class="stat-value">2,847</div>
                <div class="stat-change">+127 this week</div>
                <div class="progress-bar">
                    <div class="progress-fill w-68"></div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-header">
                    <div class="stat-title">Study Streak</div>
                    <div class="stat-icon">炎</div>
                </div>
                <div class="stat-value">23 days</div>
                <div class="stat-change">Personal best!</div>
                <div class="progress-bar">
                    <div class="progress-fill w-85"></div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-header">
                    <div class="stat-title">Lessons Completed</div>
                    <div class="stat-icon">本</div>
                </div>
                <div class="stat-value">156</div>
                <div class="stat-change">+8 this week</div>
                <div class="progress-bar">
                    <div class="progress-fill w-45"></div>
                </div>
            </div>
            <div class="stat-card">
                <div class="stat-header">
                    <div class="stat-title">Time Studied</div>
                    <div class="stat-icon">時</div>
                </div>
                <div class="stat-value">47h 32m</div>
                <div class="stat-change">+5h this week</div>
                <div class="progress-bar">
                    <div class="progress-fill w-72"></div>
                </div>
            </div>
        </div>

        <!-- Learning Heatmap -->
        <div class="heatmap-card">
            <div class="heatmap-header">
                <div class="heatmap-icon">統</div>
                <div>
                    <div class="heatmap-title">Learning Activity</div>
                    <div class="heatmap-subtitle">Your daily learning streak over the past year</div>
                </div>
            </div>
            <div class="heatmap-grid">
                <script>
                    (function(){
                      function renderHeatmap(){
                        var heatmapGrid = document.querySelector('.heatmap-grid');
                        if (!heatmapGrid) return;
                        if (heatmapGrid.children.length > 0) return;
                        for (var week = 0; week < 52; week++) {
                          var weekDiv = document.createElement('div');
                          weekDiv.className = 'heatmap-week';
                          for (var day = 0; day < 7; day++) {
                            var dayDiv = document.createElement('div');
                            var level = Math.floor(Math.random() * 5);
                            dayDiv.className = 'heatmap-day level-' + level;
                            dayDiv.title = 'Day ' + (week*7 + day + 1) + ': ' + Math.floor(Math.random() * 20) + ' words learned';
                            weekDiv.appendChild(dayDiv);
                          }
                          heatmapGrid.appendChild(weekDiv);
                        }
                      }
                      if (document.readyState === 'loading') {
                        document.addEventListener('DOMContentLoaded', renderHeatmap);
                      } else { renderHeatmap(); }
                      document.addEventListener('htmx:afterSwap', renderHeatmap);
                    })();
                </script>
            </div>
            <div class="heatmap-legend">
                <span>Less</span>
                <div class="legend-scale">
                    <div class="legend-item level-0"></div>
                    <div class="legend-item level-1"></div>
                    <div class="legend-item level-2"></div>
                    <div class="legend-item level-3"></div>
                    <div class="legend-item level-4"></div>
                </div>
                <span>More</span>
            </div>
        </div>

        <!-- Bottom Grid -->
        <div class="bottom-grid">
            <!-- Recent Achievements -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">賞</div>
                    <div class="card-title">Recent Achievements</div>
                </div>
                <div class="achievement-item">
                    <div class="achievement-icon">漢</div>
                    <div class="achievement-text">
                        <div class="achievement-title">Kanji Master</div>
                        <div class="achievement-desc">Learned 100 kanji characters</div>
                    </div>
                    <div class="achievement-badge">New!</div>
                </div>
                <div class="achievement-item">
                    <div class="achievement-icon">炎</div>
                    <div class="achievement-text">
                        <div class="achievement-title">Study Streak</div>
                        <div class="achievement-desc">23 days in a row</div>
                    </div>
                </div>
                <div class="achievement-item">
                    <div class="achievement-icon">語</div>
                    <div class="achievement-text">
                        <div class="achievement-title">Vocabulary Builder</div>
                        <div class="achievement-desc">Mastered 500 words</div>
                    </div>
                </div>
            </div>

            <!-- Learning Goals -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">目</div>
                    <div class="card-title">Learning Goals</div>
                </div>
                <div class="goal-item">
                    <div class="goal-header">
                        <span class="goal-name">Daily Words Goal</span>
                        <span class="goal-progress">18/20</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill w-90"></div>
                    </div>
                </div>
                <div class="goal-item">
                    <div class="goal-header">
                        <span class="goal-name">Weekly Study Time</span>
                        <span class="goal-progress">5.2/7 hours</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill w-74"></div>
                    </div>
                </div>
                <div class="goal-item">
                    <div class="goal-header">
                        <span class="goal-name">Monthly Lessons</span>
                        <span class="goal-progress">12/15</span>
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill w-80"></div>
                    </div>
                </div>
            </div>

            <!-- Quick Actions -->
            <div class="card">
                <div class="card-header">
                    <div class="card-icon">速</div>
                    <div class="card-title">Quick Actions</div>
                </div>
                <div class="quick-actions">
                    <button class="quick-action">
                        <span class="action-kanji">本</span>
                        <span class="action-text">Practice</span>
                    </button>
                    <button class="quick-action">
                        <span class="action-kanji">聞</span>
                        <span class="action-text">Listen</span>
                    </button>
                    <button class="quick-action">
                        <span class="action-kanji">書</span>
                        <span class="action-text">Write</span>
                    </button>
                    <button class="quick-action">
                        <span class="action-kanji">話</span>
                        <span class="action-text">Speak</span>
                    </button>
                </div>
            </div>
        </div>
    </div>
</main>

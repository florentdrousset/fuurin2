<svelte:head>
  <title>ふうりん - Dashboard</title>
</svelte:head>

<!-- Reuse the dashboard.html body content, lightly adapted to internal / routes -->

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
            <a href="/" class="nav-item">
                <div class="nav-icon">家</div>
                <div class="nav-text">
                    <div class="nav-name">Home</div>
                    <div class="nav-desc">Dashboard</div>
                </div>
            </a>
            <a href="/dashboard" class="nav-item active">
                <div class="nav-icon">板</div>
                <div class="nav-text">
                    <div class="nav-name">Dashboard</div>
                    <div class="nav-desc">Overview</div>
                </div>
                <div class="active-indicator"></div>
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
<main class="main-content">
    <div class="content-wrapper">
        <div class="welcome-section">
            <h1 class="welcome-title">ダッシュボード</h1>
            <h2 class="welcome-subtitle">Your Learning Analytics</h2>
            <p class="welcome-description">
                Track your progress, analyze your study patterns, and discover insights about your Japanese learning journey.
            </p>
        </div>

        <!-- Recent Entries Table -->
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">
                    <div class="card-icon">履</div>
                    Recent Entries
                </h3>
            </div>
            <div class="card-content">
                <div class="table-container">
                    <table class="table">
                        <thead>
                        <tr>
                            <th>Date</th>
                            <th>Activity</th>
                            <th>Words</th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                            <td class="date-cell">2025-08-26</td>
                            <td class="activity-cell">Spent 15 minutes on 'Amakano 2'</td>
                            <td class="words-cell">-</td>
                        </tr>
                        <tr>
                            <td class="date-cell">2025-08-26</td>
                            <td class="activity-cell">Spent 12 minutes on 'Amakano 2'</td>
                            <td class="words-cell">-</td>
                        </tr>
                        <tr>
                            <td class="date-cell">2025-08-20</td>
                            <td class="activity-cell">Spent 23 minutes on 'Amakano 2'</td>
                            <td class="words-cell">-</td>
                        </tr>
                        <tr>
                            <td class="date-cell">2025-08-15</td>
                            <td class="activity-cell">Spent 2 minutes on 'Amakano 2'</td>
                            <td class="words-cell">-</td>
                        </tr>
                        <tr>
                            <td class="date-cell">2025-08-13</td>
                            <td class="activity-cell">Read 32 pages of 'Spy x Family'</td>
                            <td class="words-cell">-</td>
                        </tr>
                        <tr>
                            <td class="date-cell">2025-08-12</td>
                            <td class="activity-cell">Completed vocabulary review</td>
                            <td class="words-cell">45</td>
                        </tr>
                        <tr>
                            <td class="date-cell">2025-08-11</td>
                            <td class="activity-cell">Watched anime episode with subtitles</td>
                            <td class="words-cell">23</td>
                        </tr>
                        <tr>
                            <td class="date-cell">2025-08-10</td>
                            <td class="activity-cell">Read manga chapter</td>
                            <td class="words-cell">67</td>
                        </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- Charts Grid -->
        <div class="charts-grid">
            <!-- Media Consumption Pie Chart -->
            <div class="card">
                <div class="card-header">
                    <h3 class="card-title">
                        <div class="card-icon">媒</div>
                        Media Consumption
                    </h3>
                </div>
                <div class="card-content">
                    <div class="pie-chart-container">
                        <svg class="pie-chart" viewBox="0 0 100 100">
                            <circle cx="50" cy="50" r="15.915" fill="transparent" stroke="#06b6d4" stroke-width="12"
                                    stroke-dasharray="25.13 100.53" stroke-dashoffset="0" class="pie-slice"/>
                            <circle cx="50" cy="50" r="15.915" fill="transparent" stroke="#ec4899" stroke-width="12"
                                    stroke-dasharray="37.19 100.53" stroke-dashoffset="-25.13" class="pie-slice"/>
                            <circle cx="50" cy="50" r="15.915" fill="transparent" stroke="#6b7280" stroke-width="12"
                                    stroke-dasharray="17.09 100.53" stroke-dashoffset="-62.32" class="pie-slice"/>
                            <circle cx="50" cy="50" r="15.915" fill="transparent" stroke="#3b82f6" stroke-width="12"
                                    stroke-dasharray="21.11 100.53" stroke-dashoffset="-79.41" class="pie-slice"/>
                        </svg>
                    </div>
                    <div class="legend">
                        <div class="legend-item">
                            <div class="legend-label">
                                <div class="legend-color" style="background: #06b6d4;"></div>
                                Books
                            </div>
                            <div class="legend-value">12 items (25%)</div>
                        </div>
                        <div class="legend-item">
                            <div class="legend-label">
                                <div class="legend-color" style="background: #ec4899;"></div>
                                Manga
                            </div>
                            <div class="legend-value">18 items (37%)</div>
                        </div>
                        <div class="legend-item">
                            <div class="legend-label">
                                <div class="legend-color" style="background: #6b7280;"></div>
                                Video Games
                            </div>
                            <div class="legend-value">8 items (17%)</div>
                        </div>
                        <div class="legend-item">
                            <div class="legend-label">
                                <div class="legend-color" style="background: #3b82f6;"></div>
                                Anime
                            </div>
                            <div class="legend-value">10 items (21%)</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Weekly Study Time bars (static mimic) -->
            <div class="card">
                <div class="card-header">
                    <div style="display: flex; align-items: center; justify-content: space-between;">
                        <h3 class="card-title">
                            <div class="card-icon">時</div>
                            Weekly Study Time
                        </h3>
                        <div class="week-nav">
                            <button class="week-nav-button">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M15 18l-6-6 6-6"/>
                                </svg>
                            </button>
                            <span class="week-nav-label">Aug 19-25</span>
                            <button class="week-nav-button">
                                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                    <path d="M9 18l6-6-6-6"/>
                                </svg>
                            </button>
                        </div>
                    </div>
                </div>
                <div class="card-content">
                    <div class="bar-chart">
                        <div class="bar-container">
                            <div class="bar-fill" style="height: 50%;">
                                <div class="bar-inner"></div>
                            </div>
                            <div class="bar-label">Mon</div>
                            <div class="bar-value">45m</div>
                        </div>
                        <div class="bar-container">
                            <div class="bar-fill" style="height: 35.6%;">
                                <div class="bar-inner"></div>
                            </div>
                            <div class="bar-label">Tue</div>
                            <div class="bar-value">32m</div>
                        </div>
                        <div class="bar-container">
                            <div class="bar-fill" style="height: 74.4%;">
                                <div class="bar-inner"></div>
                            </div>
                            <div class="bar-label">Wed</div>
                            <div class="bar-value">67m</div>
                        </div>
                        <div class="bar-container">
                            <div class="bar-fill" style="height: 25.6%;">
                                <div class="bar-inner"></div>
                            </div>
                            <div class="bar-label">Thu</div>
                            <div class="bar-value">23m</div>
                        </div>
                        <div class="bar-container">
                            <div class="bar-fill" style="height: 98.9%;">
                                <div class="bar-inner"></div>
                            </div>
                            <div class="bar-label">Fri</div>
                            <div class="bar-value">89m</div>
                        </div>
                        <div class="bar-container">
                            <div class="bar-fill" style="height: 62.2%;">
                                <div class="bar-inner"></div>
                            </div>
                            <div class="bar-label">Sat</div>
                            <div class="bar-value">56m</div>
                        </div>
                        <div class="bar-container">
                            <div class="bar-fill" style="height: 37.8%;">
                                <div class="bar-inner"></div>
                            </div>
                            <div class="bar-label">Sun</div>
                            <div class="bar-value">34m</div>
                        </div>
                    </div>
                    <div class="chart-summary">
                        <div class="chart-summary-main">Total: 346 minutes</div>
                        <div class="chart-summary-sub">Average: 49 min/day</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Reading Speed Chart -->
        <div class="card">
            <div class="card-header">
                <h3 class="card-title">
                    <div class="card-icon">速</div>
                    Reading Speed by Work
                </h3>
            </div>
            <div class="card-content">
                <div class="line-chart-container">
                    <div class="y-axis-label">Characters/min</div>
                    <div class="chart-area">
                        <div class="grid-lines">
                            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
                            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
                            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
                            <div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div><div class="grid-cell"></div>
                        </div>
                        <svg class="chart-svg" viewBox="0 0 100 100" preserveAspectRatio="none">
                            <polyline class="chart-line" stroke="#06b6d4"
                                      points="0,71 11,68 22,63 33,66 44,57 55,51 66,63 77,43 88,49 100,37"/>
                            <polyline class="chart-line" stroke="#ec4899"
                                      points="0,63 11,57 22,49 33,60 44,43 55,37 66,49 77,29 88,37 100,20"/>
                            <polyline class="chart-line" stroke="#6b7280"
                                      points="0,89 11,83 22,77 33,86 44,71 55,66 66,77 77,63 88,69 100,54"/>

                            <circle class="chart-point" cx="0" cy="71" r="2" fill="#06b6d4"/>
                            <circle class="chart-point" cx="11" cy="68" r="2" fill="#06b6d4"/>
                            <circle class="chart-point" cx="22" cy="63" r="2" fill="#06b6d4"/>
                            <circle class="chart-point" cx="33" cy="66" r="2" fill="#06b6d4"/>
                            <circle class="chart-point" cx="44" cy="57" r="2" fill="#06b6d4"/>
                            <circle class="chart-point" cx="55" cy="51" r="2" fill="#06b6d4"/>
                            <circle class="chart-point" cx="66" cy="63" r="2" fill="#06b6d4"/>
                            <circle class="chart-point" cx="77" cy="43" r="2" fill="#06b6d4"/>
                            <circle class="chart-point" cx="88" cy="49" r="2" fill="#06b6d4"/>
                            <circle class="chart-point" cx="100" cy="37" r="2" fill="#06b6d4"/>

                            <circle class="chart-point" cx="0" cy="63" r="2" fill="#ec4899"/>
                            <circle class="chart-point" cx="11" cy="57" r="2" fill="#ec4899"/>
                            <circle class="chart-point" cx="22" cy="49" r="2" fill="#ec4899"/>
                            <circle class="chart-point" cx="33" cy="60" r="2" fill="#ec4899"/>
                            <circle class="chart-point" cx="44" cy="43" r="2" fill="#ec4899"/>
                            <circle class="chart-point" cx="55" cy="37" r="2" fill="#ec4899"/>
                            <circle class="chart-point" cx="66" cy="49" r="2" fill="#ec4899"/>
                            <circle class="chart-point" cx="77" cy="29" r="2" fill="#ec4899"/>
                            <circle class="chart-point" cx="88" cy="37" r="2" fill="#ec4899"/>
                            <circle class="chart-point" cx="100" cy="20" r="2" fill="#ec4899"/>

                            <circle class="chart-point" cx="0" cy="89" r="2" fill="#6b7280"/>
                            <circle class="chart-point" cx="11" cy="83" r="2" fill="#6b7280"/>
                            <circle class="chart-point" cx="22" cy="77" r="2" fill="#6b7280"/>
                            <circle class="chart-point" cx="33" cy="86" r="2" fill="#6b7280"/>
                            <circle class="chart-point" cx="44" cy="71" r="2" fill="#6b7280"/>
                            <circle class="chart-point" cx="55" cy="66" r="2" fill="#6b7280"/>
                            <circle class="chart-point" cx="66" cy="77" r="2" fill="#6b7280"/>
                            <circle class="chart-point" cx="77" cy="63" r="2" fill="#6b7280"/>
                            <circle class="chart-point" cx="88" cy="69" r="2" fill="#6b7280"/>
                            <circle class="chart-point" cx="100" cy="54" r="2" fill="#6b7280"/>
                        </svg>
                    </div>
                    <div class="chart-legend">
                        <div class="legend-label">
                            <div class="legend-color" style="background: #06b6d4;"></div>
                            Spy x Family
                        </div>
                        <div class="legend-label">
                            <div class="legend-color" style="background: #ec4899;"></div>
                            Naruto
                        </div>
                        <div class="legend-label">
                            <div class="legend-color" style="background: #6b7280;"></div>
                            Berserk
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</main>

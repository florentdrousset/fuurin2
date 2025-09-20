<svelte:head>
  <title>Activity Feed - ふうりん</title>
</svelte:head>

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
            <a href="/activity-feed" class="nav-item active">
                <div class="nav-icon">活</div>
                <div class="nav-text">
                    <div class="nav-name">Feed</div>
                    <div class="nav-desc">Recent</div>
                </div>
                <div class="active-indicator"></div>
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

<main class="main-content" id="content">
    <div class="content-wrapper">
        <div class="page-header">
            <h1 class="page-title">Activity Feed</h1>
            <div class="tabs-container">
                <div class="tab active">All Activities</div>
                <div class="tab">Following</div>
                <div class="tab">My Activities</div>
            </div>
            <div class="controls">
                <button class="refresh-button">Refresh</button>
                <div class="filter-info">
                    Filter by user:
                    <span class="filter-tag">floflo</span>
                </div>
            </div>
        </div>

        <div class="activity-list">
            <div class="activity-item">
                <div class="activity-content">
                    <div class="activity-avatar">F</div>
                    <div class="activity-details">
                        <div class="activity-header">
                            <span class="activity-username">floflo</span>
                            <span class="activity-timestamp">2 days ago</span>
                        </div>
                        <div class="activity-text">engaged with 'Amakano 2'</div>
                        <div class="activity-actions">
                            <button class="action-button love">
                                <div class="action-icon">愛</div>
                                <span>0</span>
                            </button>
                            <button class="action-button comment">
                                <div class="action-icon">話</div>
                                <span>0</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="activity-item">
                <div class="activity-content">
                    <div class="activity-avatar">F</div>
                    <div class="activity-details">
                        <div class="activity-header">
                            <span class="activity-username">floflo</span>
                            <span class="activity-timestamp">2 days ago</span>
                        </div>
                        <div class="activity-text">engaged with 'Amakano 2'</div>
                        <div class="activity-actions">
                            <button class="action-button love">
                                <div class="action-icon">愛</div>
                                <span>0</span>
                            </button>
                            <button class="action-button comment">
                                <div class="action-icon">話</div>
                                <span>0</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="activity-item">
                <div class="activity-content">
                    <div class="activity-avatar">F</div>
                    <div class="activity-details">
                        <div class="activity-header">
                            <span class="activity-username">floflo</span>
                            <span class="activity-timestamp">5 days ago</span>
                        </div>
                        <div class="activity-text">engaged with 'Amakano 2'</div>
                        <div class="activity-actions">
                            <button class="action-button love">
                                <div class="action-icon">愛</div>
                                <span>0</span>
                            </button>
                            <button class="action-button comment">
                                <div class="action-icon">話</div>
                                <span>0</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="activity-item">
                <div class="activity-content">
                    <div class="activity-avatar">F</div>
                    <div class="activity-details">
                        <div class="activity-header">
                            <span class="activity-username">floflo</span>
                            <span class="activity-timestamp">1 week ago</span>
                        </div>
                        <div class="activity-text">engaged with 'Amakano 2'</div>
                        <div class="activity-actions">
                            <button class="action-button love">
                                <div class="action-icon">愛</div>
                                <span>0</span>
                            </button>
                            <button class="action-button comment">
                                <div class="action-icon">話</div>
                                <span>0</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <div class="activity-item">
                <div class="activity-content">
                    <div class="activity-avatar">F</div>
                    <div class="activity-details">
                        <div class="activity-header">
                            <span class="activity-username">floflo</span>
                            <span class="activity-timestamp">2 weeks ago</span>
                        </div>
                        <div class="activity-text">Read 32 pages of 'Spy x Family'</div>
                        <div class="activity-actions">
                            <button class="action-button love">
                                <div class="action-icon">愛</div>
                                <span>0</span>
                            </button>
                            <button class="action-button comment">
                                <div class="action-icon">話</div>
                                <span>0</span>
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</main>

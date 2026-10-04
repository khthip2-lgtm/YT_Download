/**
 * YouTube Downloader - Modern Client Web Application
 * Features: LocalStorage History, Preferences, Real-time Progress, Multi-theme
 */

// ==========================================
// 1. CONSTANTS & LOCAL STORAGE KEYS
// ==========================================
const API_BASE = window.location.origin;

const STORAGE_KEYS = {
  PREFS: 'ytdl_preferences_v1',
  HISTORY: 'ytdl_history_v1',
  RECENT_URLS: 'ytdl_recent_urls_v1',
};

const DEFAULT_PREFS = {
  theme: 'dark',
  defaultFormat: 'MP4',
  defaultQuality: 'best',
  autoDownload: true,
  autoClear: false,
};

// ==========================================
// 2. DOM ELEMENTS
// ==========================================
// Navigation & Theme
const navTabs = document.querySelectorAll('.nav-tab');
const tabPanes = document.querySelectorAll('.tab-pane');
const btnQuickTheme = document.getElementById('btnQuickTheme');
const historyBadge = document.getElementById('historyBadge');

// Downloader Elements
const videoUrlInput = document.getElementById('videoUrl');
const btnClearInput = document.getElementById('btnClearInput');
const btnPasteInput = document.getElementById('btnPasteInput');
const btnFetchInfo = document.getElementById('btnFetchInfo');
const statusAlert = document.getElementById('statusAlert');
const recentContainer = document.getElementById('recentContainer');
const recentChips = document.getElementById('recentChips');
const btnClearRecent = document.getElementById('btnClearRecent');

// Video Info Preview
const infoCard = document.getElementById('infoCard');
const videoThumbnail = document.getElementById('videoThumbnail');
const videoTitle = document.getElementById('videoTitle');
const uploaderText = document.getElementById('uploaderText');
const viewsText = document.getElementById('viewsText');
const videoDurationBadge = document.getElementById('videoDurationBadge');
const formatSelect = document.getElementById('formatSelect');
const qualitySelect = document.getElementById('qualitySelect');
const qualityGroup = document.getElementById('qualityGroup');
const btnStartDownload = document.getElementById('btnStartDownload');

// Progress Card
const progressCard = document.getElementById('progressCard');
const progressBarFill = document.getElementById('progressBarFill');
const progressPercent = document.getElementById('progressPercent');
const progressSpeed = document.getElementById('progressSpeed');
const progressEta = document.getElementById('progressEta');
const statusLabel = document.getElementById('statusLabel');
const downloadAction = document.getElementById('downloadAction');
const btnDownloadFile = document.getElementById('btnDownloadFile');

// History Elements
const historySearchInput = document.getElementById('historySearchInput');
const historyList = document.getElementById('historyList');
const historyEmpty = document.getElementById('historyEmpty');
const btnClearAllHistory = document.getElementById('btnClearAllHistory');

// Settings Elements
const settingTheme = document.getElementById('settingTheme');
const settingDefaultFormat = document.getElementById('settingDefaultFormat');
const settingDefaultQuality = document.getElementById('settingDefaultQuality');
const settingAutoDownload = document.getElementById('settingAutoDownload');
const settingAutoClear = document.getElementById('settingAutoClear');
const storageUsageText = document.getElementById('storageUsageText');
const btnResetLocalStorage = document.getElementById('btnResetLocalStorage');

// Toast Container
const toastContainer = document.getElementById('toastContainer');

// State Variables
let currentVideoData = null;
let activeJobId = null;
let pollInterval = null;

// ==========================================
// 3. STORAGE HELPERS
// ==========================================
function getPreferences() {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.PREFS);
    return raw ? { ...DEFAULT_PREFS, ...JSON.parse(raw) } : { ...DEFAULT_PREFS };
  } catch (e) {
    console.error('Error loading preferences:', e);
    return { ...DEFAULT_PREFS };
  }
}

function savePreferences(prefs) {
  try {
    localStorage.setItem(STORAGE_KEYS.PREFS, JSON.stringify(prefs));
    updateStorageStats();
  } catch (e) {
    console.error('Error saving preferences:', e);
  }
}

function getHistory() {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.HISTORY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    console.error('Error loading history:', e);
    return [];
  }
}

function saveHistory(historyList) {
  try {
    localStorage.setItem(STORAGE_KEYS.HISTORY, JSON.stringify(historyList));
    updateHistoryBadge();
    updateStorageStats();
  } catch (e) {
    console.error('Error saving history:', e);
  }
}

function addHistoryItem(item) {
  const history = getHistory();
  // Filter out duplicates with the same URL and format
  const filtered = history.filter(
    (h) => !(h.url === item.url && h.format === item.format && h.quality === item.quality)
  );
  // Add new item at beginning (most recent first, limit to 50)
  filtered.unshift(item);
  const trimmed = filtered.slice(0, 50);
  saveHistory(trimmed);
  renderHistory();
}

function getRecentUrls() {
  try {
    const raw = localStorage.getItem(STORAGE_KEYS.RECENT_URLS);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    return [];
  }
}

function saveRecentUrl(url, title) {
  if (!url) return;
  const recents = getRecentUrls().filter((r) => r.url !== url);
  recents.unshift({ url, title: title || url, date: Date.now() });
  try {
    localStorage.setItem(STORAGE_KEYS.RECENT_URLS, JSON.stringify(recents.slice(0, 6)));
    renderRecentUrls();
    updateStorageStats();
  } catch (e) {
    console.error('Error saving recent URL:', e);
  }
}

function calculateStorageSize() {
  let totalBytes = 0;
  for (let key in localStorage) {
    if (localStorage.hasOwnProperty(key)) {
      totalBytes += (localStorage[key].length + key.length) * 2;
    }
  }
  return totalBytes;
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  return `${(bytes / 1024).toFixed(1)} KB`;
}

function updateStorageStats() {
  if (!storageUsageText) return;
  const bytes = calculateStorageSize();
  const historyCount = getHistory().length;
  storageUsageText.textContent = `បានប្រើប្រាស់ ${formatBytes(bytes)} (${historyCount} វីដេអូក្នុងប្រវត្តិ)`;
}

// ==========================================
// 4. TOAST & ALERT NOTIFICATIONS
// ==========================================
function showToast(message, type = 'info') {
  if (!toastContainer) return;
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  
  const icon = type === 'success' ? '✅' : type === 'error' ? '❌' : 'ℹ️';
  toast.innerHTML = `<span>${icon}</span><span>${message}</span>`;
  
  toastContainer.appendChild(toast);
  setTimeout(() => {
    toast.remove();
  }, 3000);
}

function showAlert(message, type = 'error') {
  statusAlert.textContent = message;
  statusAlert.className = `alert alert-${type}`;
  statusAlert.classList.remove('hidden');
}

function hideAlert() {
  statusAlert.classList.add('hidden');
}

// ==========================================
// 5. THEME & TABS CONTROLLERS
// ==========================================
function applyTheme(theme) {
  document.body.setAttribute('data-theme', theme);
  const metaTheme = document.getElementById('metaThemeColor');
  if (metaTheme) {
    metaTheme.setAttribute(
      'content',
      theme === 'light' ? '#f1f5f9' : theme === 'oled' ? '#000000' : '#0b0f19'
    );
  }
  if (btnQuickTheme) {
    btnQuickTheme.querySelector('.theme-icon').textContent =
      theme === 'light' ? '☀️' : theme === 'oled' ? '⚫' : '🌙';
  }
  if (settingTheme) {
    settingTheme.value = theme;
  }
}

function switchTab(tabId) {
  navTabs.forEach((tab) => {
    const isTarget = tab.getAttribute('data-tab') === tabId;
    tab.classList.toggle('active', isTarget);
    tab.setAttribute('aria-selected', isTarget ? 'true' : 'false');
  });

  tabPanes.forEach((pane) => {
    pane.classList.toggle('active', pane.id === tabId);
  });

  if (tabId === 'tab-history') {
    renderHistory();
  }
  if (tabId === 'tab-settings') {
    updateStorageStats();
  }
}

// ==========================================
// 6. UI RENDERING FUNCTIONS
// ==========================================
function updateHistoryBadge() {
  const count = getHistory().length;
  if (historyBadge) {
    historyBadge.textContent = count;
    historyBadge.style.display = count > 0 ? 'inline-block' : 'none';
  }
}

function renderRecentUrls() {
  const recents = getRecentUrls();
  if (!recentChips || !recentContainer) return;

  if (recents.length === 0) {
    recentContainer.classList.add('hidden');
    return;
  }

  recentContainer.classList.remove('hidden');
  recentChips.innerHTML = '';

  recents.forEach((item) => {
    const chip = document.createElement('button');
    chip.className = 'recent-chip';
    chip.title = item.url;
    chip.textContent = item.title || item.url;
    chip.addEventListener('click', () => {
      videoUrlInput.value = item.url;
      updateInputClearBtn();
      btnFetchInfo.click();
    });
    recentChips.appendChild(chip);
  });
}

function renderHistory(filterText = '') {
  const history = getHistory();
  if (!historyList || !historyEmpty) return;

  const query = filterText.toLowerCase().trim();
  const items = query
    ? history.filter(
        (item) =>
          (item.title && item.title.toLowerCase().includes(query)) ||
          (item.uploader && item.uploader.toLowerCase().includes(query)) ||
          (item.format && item.format.toLowerCase().includes(query))
      )
    : history;

  if (items.length === 0) {
    historyList.innerHTML = '';
    historyEmpty.classList.remove('hidden');
    return;
  }

  historyEmpty.classList.add('hidden');
  historyList.innerHTML = items
    .map(
      (item, idx) => `
      <div class="history-item-card" data-index="${idx}">
        <img class="history-thumb" src="${item.thumbnail || 'https://via.placeholder.com/120x68?text=Video'}" alt="Thumb" loading="lazy">
        <div class="history-content">
          <h4 class="history-item-title" title="${item.title}">${item.title}</h4>
          <div class="history-item-meta">
            <span class="badge-fmt">${item.format || 'MP4'}</span>
            <span class="badge-qty">${item.quality ? item.quality + 'p' : 'Best'}</span>
            <span>• ${item.uploader || 'YouTube'}</span>
            <span>• ${item.duration_string || ''}</span>
          </div>
        </div>
        <div class="history-actions">
          <button class="btn-history-action" title="ទាញយកវីដេអូនេះម្តងទៀត" onclick="reDownloadFromHistory('${encodeURIComponent(item.url)}')">
            🔄
          </button>
          <button class="btn-history-action" title="ចម្លង Link" onclick="copyToClipboard('${item.url}')">
            🔗
          </button>
          <button class="btn-history-action btn-del" title="លុបពីប្រវត្តិ" onclick="deleteHistoryItem(${idx})">
            🗑️
          </button>
        </div>
      </div>
    `
    )
    .join('');
}

window.reDownloadFromHistory = function (encodedUrl) {
  const url = decodeURIComponent(encodedUrl);
  switchTab('tab-download');
  videoUrlInput.value = url;
  updateInputClearBtn();
  btnFetchInfo.click();
  showToast('បានផ្ទុកតំណភ្ជាប់ពីប្រវត្តិ', 'info');
};

window.copyToClipboard = async function (text) {
  try {
    await navigator.clipboard.writeText(text);
    showToast('បានចម្លង URL ទៅកាន់ Clipboard!', 'success');
  } catch (err) {
    showToast('មិនអាចចម្លងបានទេ', 'error');
  }
};

window.deleteHistoryItem = function (index) {
  const history = getHistory();
  history.splice(index, 1);
  saveHistory(history);
  renderHistory(historySearchInput ? historySearchInput.value : '');
  showToast('បានលុបមួយធាតុចេញពីប្រវត្តិ', 'info');
};

function updateInputClearBtn() {
  if (!btnClearInput) return;
  if (videoUrlInput.value.length > 0) {
    btnClearInput.classList.remove('hidden');
  } else {
    btnClearInput.classList.add('hidden');
  }
}

// ==========================================
// 7. DOWNLOADER FLOW & API INTERACTION
// ==========================================

// Toggle Format Change (Hide Quality if Audio)
formatSelect.addEventListener('change', () => {
  const fmt = formatSelect.value;
  if (fmt === 'MP3' || fmt === 'M4A') {
    qualityGroup.classList.add('hidden');
  } else {
    qualityGroup.classList.remove('hidden');
  }
});

// Step 1: Fetch Video Info
btnFetchInfo.addEventListener('click', async () => {
  const url = videoUrlInput.value.trim();
  hideAlert();

  if (!url) {
    showAlert('សូមបញ្ចូល (Paste) URL វីដេអូ YouTube ជាមុនសិន!');
    return;
  }

  // Set Loading
  btnFetchInfo.disabled = true;
  const btnText = btnFetchInfo.querySelector('.btn-text');
  const spinner = btnFetchInfo.querySelector('.spinner');
  if (btnText) btnText.textContent = 'កំពុងពិនិត្យ...';
  if (spinner) spinner.classList.remove('hidden');

  infoCard.classList.add('hidden');
  progressCard.classList.add('hidden');

  try {
    const response = await fetch(`${API_BASE}/api/info`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'មិនអាចទាញយកព័ត៌មានវីដេអូបានទេ');
    }

    currentVideoData = data;
    saveRecentUrl(url, data.title);

    // Populate Video Card
    videoThumbnail.src = data.thumbnail || 'https://via.placeholder.com/320x180?text=No+Thumbnail';
    videoTitle.textContent = data.title;
    uploaderText.textContent = data.uploader || 'YouTube Channel';
    viewsText.textContent = `${(data.view_count || 0).toLocaleString()} Views`;
    videoDurationBadge.textContent = data.duration_string || '0:00';

    // Populate Quality Dropdown
    qualitySelect.innerHTML = '<option value="">Best Quality (គុណភាពខ្ពស់បំផុត)</option>';
    if (data.available_resolutions && data.available_resolutions.length > 0) {
      data.available_resolutions.forEach((res) => {
        const opt = document.createElement('option');
        opt.value = res;
        opt.textContent = `${res}p (HD)`;
        qualitySelect.appendChild(opt);
      });
    }

    // Apply User Default Preferences
    const prefs = getPreferences();
    if (prefs.defaultFormat && formatSelect.querySelector(`option[value="${prefs.defaultFormat}"]`)) {
      formatSelect.value = prefs.defaultFormat;
      formatSelect.dispatchEvent(new Event('change'));
    }

    infoCard.classList.remove('hidden');
    showToast('បានទាញយកព័ត៌មានវីដេអូជោគជ័យ', 'success');
  } catch (err) {
    showAlert(`កំហុស៖ ${err.message}`);
    showToast(err.message, 'error');
  } finally {
    btnFetchInfo.disabled = false;
    if (btnText) btnText.textContent = 'ពិនិត្យ Video';
    if (spinner) spinner.classList.add('hidden');
  }
});

// Step 2: Start Download
btnStartDownload.addEventListener('click', async () => {
  if (!currentVideoData) return;

  const url = videoUrlInput.value.trim();
  const format = formatSelect.value;
  const qualityVal = qualitySelect.value;
  const quality = qualityVal ? parseInt(qualityVal, 10) : null;

  hideAlert();
  btnStartDownload.disabled = true;

  try {
    const response = await fetch(`${API_BASE}/api/download`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url, format, quality }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'មិនអាចចាប់ផ្តើម Download បានទេ');
    }

    activeJobId = data.job_id;

    // Reset Progress Bar
    progressBarFill.style.width = '0%';
    progressPercent.textContent = '0.0%';
    progressSpeed.textContent = '⚡ ល្បឿន: កំពុងរៀបចំ...';
    progressEta.textContent = '⏳ នៅសល់: --s';
    statusLabel.textContent = 'កំពុងភ្ជាប់ទៅកាន់ YouTube...';
    downloadAction.classList.add('hidden');
    progressCard.classList.remove('hidden');

    // Scroll smoothly to progress card
    progressCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

    // Poll Progress
    if (pollInterval) clearInterval(pollInterval);
    pollInterval = setInterval(pollJobProgress, 1000);
  } catch (err) {
    showAlert(`កំហុស៖ ${err.message}`);
    showToast(err.message, 'error');
    btnStartDownload.disabled = false;
  }
});

// Step 3: Check Real-time Download Progress
async function pollJobProgress() {
  if (!activeJobId) return;

  try {
    const response = await fetch(`${API_BASE}/api/progress/${activeJobId}`);
    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || 'កំហុសក្នុងការពិនិត្យ Progress');
    }

    const percent = Math.min(100, Math.max(0, data.percent || 0));
    progressBarFill.style.width = `${percent}%`;
    progressPercent.textContent = `${percent.toFixed(1)}%`;

    const speedMB = data.speed ? (data.speed / 1024 / 1024).toFixed(2) : '0.00';
    const etaSec = data.eta ? Math.round(data.eta) : 0;
    progressSpeed.textContent = `⚡ ល្បឿន: ${speedMB} MB/s`;
    progressEta.textContent = `⏳ នៅសល់: ${etaSec}s`;

    if (data.status === 'downloading') {
      statusLabel.textContent = 'កំពុងទាញយកទិន្នន័យ (Downloading)...';
    } else if (data.status === 'processing') {
      statusLabel.textContent = 'កំពុងបម្លែង & បញ្ចូលសំឡេង (Processing)...';
    } else if (data.status === 'completed') {
      clearInterval(pollInterval);
      btnStartDownload.disabled = false;
      progressBarFill.style.width = '100%';
      progressPercent.textContent = '100%';
      statusLabel.textContent = 'ទាញយកបានជោគជ័យ ១០០%! 🎉';

      const downloadFileUrl = `${API_BASE}/api/file/${activeJobId}`;
      btnDownloadFile.href = downloadFileUrl;
      downloadAction.classList.remove('hidden');

      // Save into LocalStorage History
      const historyItem = {
        id: activeJobId,
        title: currentVideoData.title,
        uploader: currentVideoData.uploader,
        thumbnail: currentVideoData.thumbnail,
        duration_string: currentVideoData.duration_string,
        url: videoUrlInput.value.trim(),
        format: formatSelect.value,
        quality: qualitySelect.value,
        timestamp: Date.now(),
        downloadUrl: downloadFileUrl,
      };
      addHistoryItem(historyItem);
      showToast('ទាញយកបានជោគជ័យ និងបានកត់ត្រាទុកក្នុងប្រវត្តិ!', 'success');

      // Auto-trigger Download if enabled in preferences
      const prefs = getPreferences();
      if (prefs.autoDownload) {
        const tempLink = document.createElement('a');
        tempLink.href = downloadFileUrl;
        tempLink.setAttribute('download', '');
        document.body.appendChild(tempLink);
        tempLink.click();
        tempLink.remove();
      }

      // Auto-clear Input if enabled
      if (prefs.autoClear) {
        videoUrlInput.value = '';
        updateInputClearBtn();
      }
    } else if (data.status === 'error') {
      clearInterval(pollInterval);
      btnStartDownload.disabled = false;
      statusLabel.textContent = 'បរាជ័យក្នុងការទាញយក';
      showAlert(`Download បរាជ័យ៖ ${data.error || 'កំហុសបច្ចេកទេស'}`);
      showToast('ទាញយកបរាជ័យ សូមព្យាយាមម្តងទៀត', 'error');
    }
  } catch (err) {
    console.error('Progress Polling Error:', err);
  }
}

// ==========================================
// 8. EVENT LISTENERS INITIALIZATION
// ==========================================
function initEvents() {
  // Navigation Tabs Switching
  navTabs.forEach((tab) => {
    tab.addEventListener('click', () => {
      const tabId = tab.getAttribute('data-tab');
      switchTab(tabId);
    });
  });

  // Quick Theme Toggle Button
  if (btnQuickTheme) {
    btnQuickTheme.addEventListener('click', () => {
      const prefs = getPreferences();
      const nextTheme = prefs.theme === 'dark' ? 'light' : prefs.theme === 'light' ? 'oled' : 'dark';
      prefs.theme = nextTheme;
      savePreferences(prefs);
      applyTheme(nextTheme);
      showToast(`បានប្ដូរទៅ Theme: ${nextTheme.toUpperCase()}`, 'info');
    });
  }

  // Paste from Clipboard Button
  if (btnPasteInput) {
    btnPasteInput.addEventListener('click', async () => {
      try {
        const text = await navigator.clipboard.readText();
        if (text) {
          videoUrlInput.value = text.trim();
          updateInputClearBtn();
          btnFetchInfo.click();
        }
      } catch (err) {
        videoUrlInput.focus();
        showToast('សូមចុច Ctrl+V ដើម្បីបិទភ្ជាប់ (Paste)', 'info');
      }
    });
  }

  // Input Clear Button
  if (btnClearInput) {
    btnClearInput.addEventListener('click', () => {
      videoUrlInput.value = '';
      updateInputClearBtn();
      videoUrlInput.focus();
    });
  }

  videoUrlInput.addEventListener('input', updateInputClearBtn);

  // Clear Recent URLs
  if (btnClearRecent) {
    btnClearRecent.addEventListener('click', () => {
      localStorage.removeItem(STORAGE_KEYS.RECENT_URLS);
      renderRecentUrls();
      showToast('បានសម្អាតបញ្ជីពិនិត្យថ្មីៗ', 'info');
    });
  }

  // Search History Input
  if (historySearchInput) {
    historySearchInput.addEventListener('input', (e) => {
      renderHistory(e.target.value);
    });
  }

  // Clear All History Button
  if (btnClearAllHistory) {
    btnClearAllHistory.addEventListener('click', () => {
      if (confirm('តើអ្នកប្រាកដជាចង់សម្អាតប្រវត្តិទាញយកទាំងអស់មែនទេ?')) {
        saveHistory([]);
        renderHistory();
        showToast('បានសម្អាតប្រវត្តិទាំងអស់ជោគជ័យ', 'success');
      }
    });
  }

  // Settings Controls
  if (settingTheme) {
    settingTheme.addEventListener('change', (e) => {
      const prefs = getPreferences();
      prefs.theme = e.target.value;
      savePreferences(prefs);
      applyTheme(prefs.theme);
    });
  }

  if (settingDefaultFormat) {
    settingDefaultFormat.addEventListener('change', (e) => {
      const prefs = getPreferences();
      prefs.defaultFormat = e.target.value;
      savePreferences(prefs);
      showToast('បានរក្សាទុក Format លំនាំដើម', 'success');
    });
  }

  if (settingDefaultQuality) {
    settingDefaultQuality.addEventListener('change', (e) => {
      const prefs = getPreferences();
      prefs.defaultQuality = e.target.value;
      savePreferences(prefs);
      showToast('បានរក្សាទុក Quality លំនាំដើម', 'success');
    });
  }

  if (settingAutoDownload) {
    settingAutoDownload.addEventListener('change', (e) => {
      const prefs = getPreferences();
      prefs.autoDownload = e.target.checked;
      savePreferences(prefs);
    });
  }

  if (settingAutoClear) {
    settingAutoClear.addEventListener('change', (e) => {
      const prefs = getPreferences();
      prefs.autoClear = e.target.checked;
      savePreferences(prefs);
    });
  }

  // Reset LocalStorage
  if (btnResetLocalStorage) {
    btnResetLocalStorage.addEventListener('click', () => {
      if (confirm('តើអ្នកចង់កំណត់ការកំណត់ និងទិន្នន័យ Local Storage ឡើងវិញទាំងអស់មែនទេ?')) {
        localStorage.clear();
        applyTheme(DEFAULT_PREFS.theme);
        initPreferences();
        renderHistory();
        renderRecentUrls();
        updateStorageStats();
        showToast('បានកំណត់ Local Storage ឡើងវិញជោគជ័យ!', 'success');
      }
    });
  }
}

// ==========================================
// 9. APP INITIALIZATION
// ==========================================
function initPreferences() {
  const prefs = getPreferences();
  applyTheme(prefs.theme);

  if (settingDefaultFormat) settingDefaultFormat.value = prefs.defaultFormat;
  if (settingDefaultQuality) settingDefaultQuality.value = prefs.defaultQuality;
  if (settingAutoDownload) settingAutoDownload.checked = prefs.autoDownload;
  if (settingAutoClear) settingAutoClear.checked = prefs.autoClear;

  if (formatSelect) {
    formatSelect.value = prefs.defaultFormat;
    formatSelect.dispatchEvent(new Event('change'));
  }
}

window.addEventListener('DOMContentLoaded', () => {
  initPreferences();
  initEvents();
  renderRecentUrls();
  renderHistory();
  updateHistoryBadge();
  updateStorageStats();
});

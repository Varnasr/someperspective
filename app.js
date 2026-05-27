    // Inline fallback data (loaded from data.json when available)
    // PROJECTION_START_INDEX: indices >= this are model-projected, not observed.
    const PROJECTION_START_INDEX = 13;
    const FALLBACK_DATA = {
        economic: {
            years:               [2014,2015,2016,2017,2018,2019,2020,2021,2022,2023,2024,2025,2026,2027],
            yearLabels:          ["2014","2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025","2026","2027*"],
            gdpGrowth:           [7.4,8.0,8.2,7.2,6.1,4.2,-7.3,8.7,7.2,7.6,7.8,6.5,7.4,6.8],
            unemployment:        [4.9,5.0,5.0,6.0,6.1,5.8,7.1,4.2,4.1,3.2,3.2,3.1,5.1,5.0],
            youthUnemployment:   [13.5,13.8,14.2,15.6,16.1,14.8,17.8,13.2,12.9,12.9,12.8,12.5,12.3,12.1],
            graduateUnemployment:[18.5,19.2,21.0,23.5,25.0,23.0,31.0,25.0,22.0,29.1,28.5,27.0,26.5,26.0],
            top1Share:           [21.3,21.7,21.5,21.5,21.7,22.1,22.3,22.5,22.6,22.6,22.6,22.8,23.0,23.1],
            bottom50Share:       [15.0,14.7,14.9,14.9,14.7,13.5,13.3,13.1,13.1,13.1,13.1,13.0,12.9,12.8],
            formalEmployment:    [13.0,12.8,12.5,12.2,11.9,11.6,11.4,11.5,11.3,11.2,11.2,11.0,10.9,10.8],
            informalEmployment:  [87.0,87.2,87.5,87.8,88.1,88.4,88.6,88.5,88.7,88.8,88.8,89.0,89.1,89.2],
            pressFreedom:        [140,136,133,136,138,140,142,142,150,161,159,151,157,158],
            ssi:                 [2.3,2.5,2.4,2.4,2.6,4.8,7.2,6.8,7.0,7.5,7.8,8.0,8.2,8.3],
            fci:                 [0.62,0.64,0.66,0.68,0.70,0.72,0.84,0.78,0.76,0.77,0.78,0.79,0.80,0.81],
            dqi:                 [0.71,0.70,0.68,0.65,0.60,0.55,0.48,0.45,0.43,0.42,0.42,0.41,0.40,0.39],
            gigWorkers:          [0.8,1.2,1.8,2.5,3.2,4.1,5.2,6.0,6.8,7.3,7.7,8.2,8.8,9.4],
            ruralIncome:         [100,99,98,97,96,95,93,94,95,96,98,97,97,97],
            femaleLFPR:          [22.5,22.0,21.8,21.5,21.2,21.0,20.8,20.5,20.3,20.5,20.8,20.9,21.0,21.1]
        },
        international: {
            countries:['India','Brazil','Turkey','Hungary','South Africa'],
            vdem2014:[0.71,0.85,0.52,0.63,0.75],
            vdem2026:[0.26,0.69,0.18,0.41,0.70],
            press2014:[140,99,154,64,42],
            press2026:[157,80,159,70,38]
        }
    };

    // Tab <-> URL hash mapping
    const TAB_HASH = {
        'What is This?': 'what-is-this',
        'Executive Summary': 'executive-summary',
        'Key Findings': 'key-findings',
        'Interactive Data': 'interactive-data',
        'Correlation Explorer': 'correlation-explorer',
        'Three Indices': 'three-indices',
        'Human Stories': 'human-stories',
        'Methodology': 'methodology',
        'Implications': 'implications',
        'Era Comparison': 'era-comparison',
        'Scenario Lab': 'scenario-lab',
        'Deep Analysis': 'deep-analysis',
        'What Next?': 'what-next'
    };
    const HASH_TAB = Object.fromEntries(Object.entries(TAB_HASH).map(([k,v]) => [v,k]));

    // ECharts color palette
    const COLORS = ['#3b82f6','#ef4444','#22c55e','#f59e0b','#8b5cf6','#ec4899','#06b6d4','#f97316'];

    // Mobile detection helper
    function isMobile() { return window.innerWidth < 640; }

    // Common ECharts options — responsive
    function baseOpts(darkMode) {
        const mobile = isMobile();
        return {
            backgroundColor: 'transparent',
            textStyle: { fontFamily: "'Inter', system-ui, sans-serif", fontSize: mobile ? 11 : 12, color: darkMode ? '#e2e8f0' : '#374151' },
            animationDuration: 800,
            animationEasing: 'cubicOut',
            toolbox: mobile ? { show: false } : {
                feature: {
                    saveAsImage: { title: 'Save', pixelRatio: 2 },
                    dataView: { title: 'Data', readOnly: true, lang: ['Data View','Close','Refresh'] },
                    restore: { title: 'Reset' }
                },
                iconStyle: { borderColor: darkMode ? '#94a3b8' : '#6b7280' }
            },
            grid: mobile
                ? { left: 10, right: 10, bottom: 45, top: 50, containLabel: true }
                : { left: 60, right: 60, bottom: 80, top: 60, containLabel: true }
        };
    }

    // Responsive title helper
    function chartTitle(text, darkMode) {
        const mobile = isMobile();
        return {
            text: mobile && text.length > 40 ? text.substring(0, 38) + '...' : text,
            left: 'center', top: 0,
            textStyle: { fontSize: mobile ? 11 : 13, fontWeight: 500, color: darkMode ? '#e2e8f0' : '#374151' }
        };
    }

    // Responsive legend
    function chartLegend(data, extra) {
        const mobile = isMobile();
        return {
            data,
            top: mobile ? 20 : 25,
            textStyle: { fontSize: mobile ? 10 : 12 },
            itemWidth: mobile ? 14 : 25,
            itemHeight: mobile ? 8 : 14,
            itemGap: mobile ? 6 : 10,
            ...extra
        };
    }

    function dataZoom() {
        const mobile = isMobile();
        return mobile
            ? [{ type: 'inside' }]
            : [
                { type: 'slider', bottom: 10, height: 22, borderColor: 'transparent', backgroundColor: 'rgba(0,0,0,0.05)', fillerColor: 'rgba(59,130,246,0.15)', handleStyle: { color: '#3b82f6' } },
                { type: 'inside' }
            ];
    }

    function siteApp() {
        return {
            // State
            darkMode: false,
            themeMode: 'device', // 'light', 'dark', 'device'
            activeTab: 'What is This?',
            selectedAudience: 'Citizen',
            chartOptions: { primary: 'gdpGrowth', comparison1: '', comparison2: '' },
            charts: {},
            economicData: FALLBACK_DATA.economic,
            internationalData: FALLBACK_DATA.international,
            dataLoadError: false,
            dataUpdated: '',
            viewModes: { gdpEmployment: 'chart', formalEmployment: 'chart', inequality: 'chart' },
            tableSortCol: null,
            tableSortAsc: true,
            // New feature state
            timelineIndex: 0,
            timelinePlaying: false,
            timelineTimer: null,
            scatterX: 'gdpGrowth',
            scatterY: 'formalEmployment',
            correlationR: 0,
            eraIndicator: 'gdpGrowth',
            scenarioInputs: { formalEmp: 10.9, pressFreedom: 157, cessShare: 20.5, statsReleased: 40 },
            scenarioOutputs: { ssi: 8.2, fci: 0.80, dqi: 0.40 },

            audiences: ['Researcher', 'Policy Maker', 'Journalist', 'Citizen'],

            get tabs() {
                // Flat list (used by URL hash mapping and any code expecting an array)
                const flat = [];
                for (const g of this.tabGroups) flat.push(...g.tabs);
                if (this.featuredTab) flat.push(this.featuredTab);
                return flat;
            },
            // Featured standalone tab pinned to the end of the nav
            featuredTab: 'Deep Analysis',
            // Grouped nav structure
            tabGroups: [
                { label: 'Overview', tabs: ['What is This?', 'Executive Summary', 'Key Findings'] },
                { label: 'Explore',  tabs: ['Interactive Data', 'Correlation Explorer', 'Three Indices', 'Era Comparison', 'Human Stories'] },
                { label: 'Methods',  tabs: ['Methodology', 'Scenario Lab'] },
                { label: 'Action',   tabs: ['Implications', 'What Next?'] }
            ],
            openGroup: null,
            // True if the given group contains the currently active tab
            isGroupActive(group) { return group.tabs.includes(this.activeTab); },
            // Tabs that should display a "New" pip in the nav
            newTabs: ['Deep Analysis'],
            // Per-role recommended jumping-off points
            roleConfig: {
                'Researcher': {
                    intro: '<strong>For Researchers:</strong> Comprehensive political-economy assessment through May 2026 with three novel indices (SSI, FCI, DQI). All methodologies transparent and replicable. Raw data in CSV/JSON, replication code in R and Python.',
                    cta: 'Start with Methodology, then Deep Analysis for the regime-comparison tables.',
                    suggested: ['Methodology', 'Three Indices', 'Deep Analysis', 'Era Comparison']
                },
                'Policy Maker': {
                    intro: '<strong>For Policy Makers:</strong> Executive summary plus actionable recommendations. Priority reforms: statistical independence, fiscal federalism rebalancing, urban employment guarantee.',
                    cta: 'Start with the Executive Summary, then jump to Implications and What Next?.',
                    suggested: ['Executive Summary', 'Key Findings', 'Implications', 'What Next?']
                },
                'Journalist': {
                    intro: '<strong>For Journalists:</strong> Four ready-to-use data stories with human angles and verified quotes. All statistics fact-checked against public sources through May 2026. Visual assets exportable as PNG.',
                    cta: 'Start with Human Stories for the angle, then Three Indices for the supporting numbers.',
                    suggested: ['Human Stories', 'Key Findings', 'Three Indices', 'Interactive Data']
                },
                'Citizen': {
                    intro: '<strong>For Citizens:</strong> Plain-language explanations of what the data shows about jobs, inequality, federalism, and democratic erosion — and what each finding means for everyday life.',
                    cta: 'Start with What is This?, then read the Executive Summary and Human Stories.',
                    suggested: ['What is This?', 'Executive Summary', 'Human Stories', 'What Next?']
                }
            },

            // Backwards-compat shim: any code that read `audienceNotes[role]`
            // continues to work, but content now lives in roleConfig.
            get audienceNotes() {
                const out = {};
                for (const k of Object.keys(this.roleConfig)) out[k] = this.roleConfig[k].intro;
                return out;
            },

            // Initialize
            async init() {
                this.themeMode = localStorage.getItem('themeMode') || 'device';
                this.applyTheme();
                // Listen for device theme changes
                window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
                    if (this.themeMode === 'device') this.applyTheme();
                });
                document.documentElement.classList.add('js');

                // Remove loading skeleton
                const skeleton = document.getElementById('loading-skeleton');
                if (skeleton) skeleton.remove();

                // Load data from JSON
                try {
                    const resp = await fetch('data.json?v=' + (document.querySelector('meta[name="version"]')?.content || Date.now()), { cache: 'no-cache' });
                    if (!resp.ok) throw new Error('HTTP ' + resp.status);
                    const d = await resp.json();
                    if (d.economic) this.economicData = d.economic;
                    if (d.international) this.internationalData = d.international;
                    if (d.meta && d.meta.updated) this.dataUpdated = d.meta.updated;
                } catch(e) {
                    console.warn('data.json fetch failed; using bundled fallback values', e);
                    this.dataLoadError = true;
                }

                // URL hash routing
                const hash = window.location.hash.slice(1);
                if (hash && HASH_TAB[hash]) this.activeTab = HASH_TAB[hash];

                window.addEventListener('popstate', () => {
                    const h = window.location.hash.slice(1);
                    if (h && HASH_TAB[h]) this.activeTab = HASH_TAB[h];
                });

                // Global resize
                window.addEventListener('resize', () => {
                    Object.values(this.charts).forEach(c => c && c.resize && c.resize());
                });

                // Init charts after Alpine settles (ECharts may still be loading via defer)
                const initCharts = () => {
                    if (typeof echarts === 'undefined') {
                        setTimeout(initCharts, 100);
                        return;
                    }
                    this.initializeCharts();
                    this.initSparklines();
                };
                this.$nextTick(initCharts);

                // Tab changes: update hash + reinit charts
                this.$watch('activeTab', (tab) => {
                    window.location.hash = TAB_HASH[tab] || '';
                    this.$nextTick(() => {
                        // ECharts needs a moment for x-show to flip display
                        setTimeout(() => this.initializeCharts(), 50);
                    });
                });

                this.$watch('selectedAudience', () => {
                    this.$nextTick(() => setTimeout(() => this.initializeCharts(), 50));
                });
            },

            setTheme(mode) {
                this.themeMode = mode;
                localStorage.setItem('themeMode', mode);
                this.applyTheme();
                // Recreate all charts with new theme
                this.disposeAll();
                this.$nextTick(() => {
                    this.initializeCharts();
                    this.initSparklines();
                });
            },

            applyTheme() {
                if (this.themeMode === 'dark') {
                    this.darkMode = true;
                } else if (this.themeMode === 'light') {
                    this.darkMode = false;
                } else {
                    // device preference
                    this.darkMode = window.matchMedia('(prefers-color-scheme: dark)').matches;
                }
            },

            // Google Translate integration
            translatePage(lang) {
                if (lang === 'en') {
                    // Remove translation
                    const frame = document.querySelector('.goog-te-banner-frame');
                    if (frame) frame.remove();
                    document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;';
                    document.cookie = 'googtrans=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; domain=.' + location.hostname;
                    location.reload();
                    return;
                }
                // Set cookie and trigger translate
                document.cookie = `googtrans=/en/${lang}; path=/;`;
                document.cookie = `googtrans=/en/${lang}; path=/; domain=.${location.hostname}`;
                if (!window._googleTranslateLoaded) {
                    window.googleTranslateElementInit = function() {
                        new google.translate.TranslateElement({ pageLanguage: 'en', includedLanguages: 'hi,ta,bn,mr', autoDisplay: false }, 'google_translate_element');
                    };
                    const s = document.createElement('script');
                    s.src = 'https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit';
                    document.head.appendChild(s);
                    window._googleTranslateLoaded = true;
                } else {
                    location.reload();
                }
            },

            toggleView(key) {
                this.viewModes[key] = this.viewModes[key] === 'chart' ? 'table' : 'chart';
                if (this.viewModes[key] === 'chart') {
                    this.$nextTick(() => setTimeout(() => this.initializeCharts(), 50));
                }
            },

            // Render a sortable HTML table
            renderTable(headers, rows) {
                let html = '<table class="w-full text-sm border-collapse"><thead><tr>';
                headers.forEach((h, i) => {
                    html += `<th class="text-left py-2 px-3 border-b border-gray-200 dark:border-gray-700 font-semibold cursor-pointer hover:text-blue-600" onclick="document.dispatchEvent(new CustomEvent('sort-table',{detail:${i}}))">${h} ↕</th>`;
                });
                html += '</tr></thead><tbody>';
                rows.forEach(row => {
                    html += '<tr class="border-b border-gray-100 dark:border-gray-800 hover:bg-gray-50 dark:hover:bg-gray-800/50">';
                    row.forEach(cell => { html += `<td class="py-1.5 px-3 tabular-nums">${cell}</td>`; });
                    html += '</tr>';
                });
                html += '</tbody></table>';
                return html;
            },

            // Dispose all ECharts instances
            disposeAll() {
                Object.keys(this.charts).forEach(key => {
                    if (this.charts[key]) { this.charts[key].dispose(); delete this.charts[key]; }
                });
            },

            // Get or create an ECharts instance
            getChart(id, group) {
                if (typeof echarts === 'undefined') return null;
                const dom = document.getElementById(id);
                if (!dom || dom.offsetWidth === 0) return null;
                if (this.charts[id]) { this.charts[id].dispose(); }
                const theme = this.darkMode ? 'dark' : null;
                const chart = echarts.init(dom, theme);
                if (!dom.getAttribute('role')) dom.setAttribute('role', 'img');
                const origSetOption = chart.setOption.bind(chart);
                chart.setOption = (opt, ...rest) => {
                    if (opt && typeof opt === 'object' && !opt.aria) opt.aria = { enabled: true };
                    return origSetOption(opt, ...rest);
                };
                this.charts[id] = chart;
                if (group) echarts.connect(group);
                return chart;
            },

            initializeCharts() {
                const tab = this.activeTab;
                if (tab === 'What is This?') {
                    this.initSparklines();
                } else if (tab === 'Key Findings') {
                    this.createGDPEmploymentChart();
                    this.createFormalEmploymentChart();
                    this.createInequalityChart();
                    echarts.connect('keyFindings');
                } else if (tab === 'Interactive Data') {
                    this.updateInteractiveChart();
                } else if (tab === 'Correlation Explorer') {
                    this.updateScatterPlot();
                } else if (tab === 'Three Indices') {
                    this.createIndicesChart();
                } else if (tab === 'Human Stories') {
                    this.createHumanStoriesCharts();
                    echarts.connect('humanStories');
                } else if (tab === 'Methodology') {
                    this.createDataCoverageChart();
                    this.createIndexRadarChart();
                } else if (tab === 'Implications') {
                    this.createInternationalChart();
                    this.createDemocraticDeclineChart();
                    this.createStateDisparitiesChart();
                } else if (tab === 'Era Comparison') {
                    this.createEraComparisonChart();
                    this.updateEraChart();
                } else if (tab === 'Scenario Lab') {
                    this.updateScenario();
                } else if (tab === 'Deep Analysis') {
                    this.createDecouplingChart();
                    if (Object.keys(this.csvData).length === 0) {
                        this.loadCSVData().then(() => this.createCSVCharts());
                    } else {
                        this.createCSVCharts();
                    }
                }
            },

            // Sparklines for stat cards
            initSparklines() {
                if (typeof echarts === 'undefined') return;
                const d = this.economicData;
                const mk = (id, data, color) => {
                    const dom = document.getElementById(id);
                    if (!dom || dom.offsetWidth === 0) return;
                    const existing = echarts.getInstanceByDom(dom);
                    if (existing) existing.dispose();
                    const c = echarts.init(dom, this.darkMode ? 'dark' : null);
                    c.setOption({
                        backgroundColor: 'transparent',
                        grid: { left: 0, right: 0, top: 2, bottom: 2 },
                        xAxis: { type: 'category', show: false, data: d.years },
                        yAxis: { type: 'value', show: false },
                        series: [{ type: 'line', data, smooth: true, symbol: 'none', lineStyle: { width: 1.5, color }, areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: color.replace(')', ',0.3)').replace('rgb', 'rgba') }, { offset: 1, color: 'transparent' }] } } }],
                        animation: false
                    });
                };
                mk('sparkWealth', d.top1Share, '#ef4444');
                mk('sparkGradUnemp', d.graduateUnemployment, '#f59e0b');
                mk('sparkPress', d.pressFreedom, '#8b5cf6');
                mk('sparkCensus', d.years.map(() => 1), '#3b82f6');
            },

            // === Chart Creation Methods ===

            createGDPEmploymentChart() {
                const c = this.getChart('gdpEmploymentChart', 'keyFindings');
                if (!c) return;
                const d = this.economicData;
                const mobile = isMobile();
                c.setOption({
                    ...baseOpts(this.darkMode),
                    tooltip: { trigger: 'axis', axisPointer: { type: mobile ? 'line' : 'cross' } },
                    legend: chartLegend(['GDP Growth (%)','Unemployment Rate (%)'], { top: 5 }),
                    xAxis: { type: 'category', data: d.years, axisLabel: { color: this.darkMode ? '#94a3b8' : '#6b7280', fontSize: mobile ? 10 : 12, rotate: mobile ? 45 : 0 } },
                    yAxis: [
                        { type: 'value', name: mobile ? 'GDP%' : 'GDP Growth (%)', nameTextStyle: { color: '#3b82f6', fontSize: mobile ? 10 : 12 }, axisLine: { lineStyle: { color: '#3b82f6' } }, axisLabel: { fontSize: mobile ? 10 : 12 } },
                        { type: 'value', name: mobile ? 'Unemp%' : 'Unemployment (%)', nameTextStyle: { color: '#ef4444', fontSize: mobile ? 10 : 12 }, axisLine: { lineStyle: { color: '#ef4444' } }, splitLine: { show: false }, axisLabel: { fontSize: mobile ? 10 : 12 } }
                    ],
                    dataZoom: dataZoom(),
                    series: [
                        { name: 'GDP Growth (%)', type: 'line', data: d.gdpGrowth, smooth: true, itemStyle: { color: '#3b82f6' }, areaStyle: { color: { type: 'linear', x:0,y:0,x2:0,y2:1, colorStops: [{offset:0,color:'rgba(59,130,246,0.2)'},{offset:1,color:'rgba(59,130,246,0)'}] } }, yAxisIndex: 0 },
                        { name: 'Unemployment Rate (%)', type: 'line', data: d.unemployment, smooth: true, itemStyle: { color: '#ef4444' }, areaStyle: { color: { type: 'linear', x:0,y:0,x2:0,y2:1, colorStops: [{offset:0,color:'rgba(239,68,68,0.15)'},{offset:1,color:'rgba(239,68,68,0)'}] } }, yAxisIndex: 1 }
                    ]
                });
            },

            createFormalEmploymentChart() {
                const c = this.getChart('formalEmploymentChart', 'keyFindings');
                if (!c) return;
                const d = this.economicData;
                c.setOption({
                    ...baseOpts(this.darkMode),
                    tooltip: { trigger: 'axis' },
                    legend: { data: ['Formal (%)','Informal (%)'], top: 5 },
                    xAxis: { type: 'category', data: d.years },
                    yAxis: { type: 'value', max: 100 },
                    dataZoom: dataZoom(),
                    series: [
                        { name: 'Formal (%)', type: 'bar', stack: 'emp', data: d.formalEmployment, itemStyle: { color: '#22c55e' }, barWidth: '60%' },
                        { name: 'Informal (%)', type: 'bar', stack: 'emp', data: d.informalEmployment, itemStyle: { color: '#ef4444' } }
                    ]
                });
            },

            createInequalityChart() {
                const c = this.getChart('inequalityChart', 'keyFindings');
                if (!c) return;
                const d = this.economicData;
                c.setOption({
                    ...baseOpts(this.darkMode),
                    title: chartTitle('Rising inequality matches colonial-era extremes', this.darkMode),
                    tooltip: { trigger: 'axis' },
                    legend: chartLegend(isMobile() ? ['Top 1%','Bottom 50%'] : ['Top 1% Income Share (%)','Bottom 50% Income Share (%)']),
                    xAxis: { type: 'category', data: d.years },
                    yAxis: { type: 'value', max: 25 },
                    dataZoom: dataZoom(),
                    series: [
                        { name: 'Top 1% Income Share (%)', type: 'line', data: d.top1Share, smooth: true, itemStyle: { color: '#ef4444' }, areaStyle: { opacity: 0.12 } },
                        { name: 'Bottom 50% Income Share (%)', type: 'line', data: d.bottom50Share, smooth: true, itemStyle: { color: '#22c55e' }, areaStyle: { opacity: 0.12 } }
                    ]
                });
            },

            createInteractiveChart() { this.updateInteractiveChart(); },

            updateInteractiveChart() {
                const c = this.getChart('interactiveChart');
                if (!c) return;
                const d = this.economicData;
                const dataMap = {
                    gdpGrowth: { label: 'GDP Growth (%)', data: d.gdpGrowth, color: '#3b82f6' },
                    unemployment: { label: 'Unemployment (%)', data: d.unemployment, color: '#ef4444' },
                    top1Share: { label: 'Top 1% Share (%)', data: d.top1Share, color: '#f59e0b' },
                    formalEmployment: { label: 'Formal Employment (%)', data: d.formalEmployment, color: '#22c55e' },
                    pressFreedom: { label: 'Press Freedom Rank', data: d.pressFreedom, color: '#8b5cf6' },
                    ssi: { label: 'SSI', data: d.ssi, color: '#ec4899' },
                    fci: { label: 'FCI ×10', data: d.fci.map(v => v*10), color: '#06b6d4' },
                    dqi: { label: 'DQI ×10', data: d.dqi.map(v => v*10), color: '#f97316' }
                };
                const series = [];
                const yAxes = [];
                const legend = [];
                const picks = [this.chartOptions.primary, this.chartOptions.comparison1, this.chartOptions.comparison2].filter(Boolean);

                picks.forEach((key, i) => {
                    const m = dataMap[key];
                    if (!m) return;
                    legend.push(m.label);
                    yAxes.push({
                        type: 'value', name: m.label, position: i === 0 ? 'left' : 'right',
                        offset: i > 1 ? 60 : 0,
                        axisLine: { show: true, lineStyle: { color: m.color } },
                        splitLine: { show: i === 0 },
                        nameTextStyle: { color: m.color }
                    });
                    series.push({
                        name: m.label, type: 'line', data: m.data, smooth: true,
                        yAxisIndex: i, itemStyle: { color: m.color },
                        lineStyle: i > 0 ? { type: 'dashed' } : {}
                    });
                });

                c.setOption({
                    ...baseOpts(this.darkMode),
                    tooltip: { trigger: 'axis', axisPointer: { type: 'cross' } },
                    legend: { data: legend, top: 5 },
                    xAxis: { type: 'category', data: d.years },
                    yAxis: yAxes.length ? yAxes : [{ type: 'value' }],
                    dataZoom: dataZoom(),
                    series
                }, true);
            },

            createIndicesChart() {
                const c = this.getChart('indicesChart');
                if (!c) return;
                const d = this.economicData;
                c.setOption({
                    ...baseOpts(this.darkMode),
                    title: chartTitle('Three Indices Show Concurrent Deterioration', this.darkMode),
                    tooltip: { trigger: 'axis' },
                    legend: chartLegend(['SSI','FCI ×10','DQI ×10']),
                    xAxis: { type: 'category', data: d.years },
                    yAxis: { type: 'value', max: 10 },
                    dataZoom: dataZoom(),
                    series: [
                        { name: 'SSI', type: 'line', data: d.ssi, smooth: true, itemStyle: { color: '#ef4444' }, areaStyle: { opacity: 0.1 } },
                        { name: 'FCI ×10', type: 'line', data: d.fci.map(v => v*10), smooth: true, itemStyle: { color: '#f59e0b' }, areaStyle: { opacity: 0.1 } },
                        { name: 'DQI ×10', type: 'line', data: d.dqi.map(v => v*10), smooth: true, itemStyle: { color: '#8b5cf6' }, areaStyle: { opacity: 0.1 } }
                    ]
                });
            },

            createHumanStoriesCharts() {
                const d = this.economicData;
                // Gig Economy
                const gig = this.getChart('gigEconomyChart', 'humanStories');
                if (gig) {
                    gig.setOption({
                        ...baseOpts(this.darkMode),
                        grid: isMobile() ? { left: 5, right: 5, bottom: 20, top: 40, containLabel: true } : { left: 40, right: 20, bottom: 30, top: 50 },
                        title: chartTitle('Gig Work Growth', this.darkMode),
                        tooltip: { trigger: 'axis' },
                        xAxis: { type: 'category', data: d.years.slice(-5) },
                        yAxis: { type: 'value' },
                        series: [{ name: 'Gig Workers (M)', type: 'bar', data: d.gigWorkers.slice(-5), itemStyle: { color: '#3b82f6', borderRadius: [4,4,0,0] } }],
                        toolbox: { show: false }
                    });
                }
                // Farmer Income
                const farmer = this.getChart('farmerIncomeChart', 'humanStories');
                if (farmer) {
                    farmer.setOption({
                        ...baseOpts(this.darkMode),
                        grid: isMobile() ? { left: 5, right: 5, bottom: 20, top: 40, containLabel: true } : { left: 40, right: 20, bottom: 30, top: 50 },
                        title: chartTitle('Declining Real Rural Incomes', this.darkMode),
                        tooltip: { trigger: 'axis' },
                        xAxis: { type: 'category', data: d.years },
                        yAxis: { type: 'value' },
                        series: [{ name: 'Real Rural Income', type: 'line', data: d.ruralIncome, smooth: true, itemStyle: { color: '#22c55e' }, areaStyle: { opacity: 0.15 } }],
                        toolbox: { show: false }
                    });
                }
                // Women LFPR
                const women = this.getChart('womenLFPRChart', 'humanStories');
                if (women) {
                    women.setOption({
                        ...baseOpts(this.darkMode),
                        grid: isMobile() ? { left: 5, right: 5, bottom: 20, top: 40, containLabel: true } : { left: 40, right: 20, bottom: 30, top: 50 },
                        title: chartTitle('Female Labor Force Participation', this.darkMode),
                        tooltip: { trigger: 'axis' },
                        xAxis: { type: 'category', data: d.years },
                        yAxis: { type: 'value', min: 19, max: 24 },
                        series: [{ name: 'Female LFPR (%)', type: 'line', data: d.femaleLFPR, smooth: true, itemStyle: { color: '#ec4899' }, areaStyle: { opacity: 0.15 } }],
                        toolbox: { show: false }
                    });
                }
            },

            createInternationalChart() {
                const c = this.getChart('internationalChart');
                if (!c) return;
                const intl = this.internationalData;
                c.setOption({
                    ...baseOpts(this.darkMode),
                    title: chartTitle('Democratic Quality: India Shows Steepest Decline', this.darkMode),
                    tooltip: { trigger: 'axis' },
                    legend: chartLegend(['V-Dem 2014','V-Dem 2026']),
                    xAxis: { type: 'category', data: intl.countries },
                    yAxis: { type: 'value', max: 1 },
                    series: [
                        { name: 'V-Dem 2014', type: 'bar', data: intl.vdem2014, itemStyle: { color: 'rgba(59,130,246,0.6)' }, barGap: '10%' },
                        { name: 'V-Dem 2026', type: 'bar', data: intl.vdem2026, itemStyle: { color: 'rgba(239,68,68,0.85)' } }
                    ]
                });
            },

            // Export chart as PNG
            exportChart(chartId, filename) {
                const chart = this.charts[chartId];
                if (!chart) return;
                const url = chart.getDataURL({ type: 'png', pixelRatio: 2, backgroundColor: this.darkMode ? '#1e293b' : '#ffffff' });
                const link = document.createElement('a');
                link.download = `${filename}-${Date.now()}.png`;
                link.href = url;
                link.click();
            },

            // Export CSV
            exportDataAsCSV() {
                const d = this.economicData;
                let csv = 'India Economic Data through May 2026\n';
                csv += 'Year,GDP Growth,Unemployment,Top 1% Share,Bottom 50% Share,Formal Employment,SSI,FCI,DQI\n';
                for (let i = 0; i < d.years.length; i++) {
                    csv += `${d.years[i]},${d.gdpGrowth[i]},${d.unemployment[i]},${d.top1Share[i]},${d.bottom50Share[i]},${d.formalEmployment[i]},${d.ssi[i]},${d.fci[i]},${d.dqi[i]}\n`;
                }
                const blob = new Blob([csv], { type: 'text/csv' });
                const link = document.createElement('a');
                link.download = `india-economic-data-mar2026-${Date.now()}.csv`;
                link.href = URL.createObjectURL(blob);
                link.click();
            },

            // ===== ANIMATED TIMELINE =====
            toggleTimeline() {
                if (this.timelinePlaying) {
                    clearInterval(this.timelineTimer);
                    this.timelinePlaying = false;
                } else {
                    if (parseInt(this.timelineIndex) >= this.economicData.years.length - 1) this.timelineIndex = 0;
                    this.timelinePlaying = true;
                    this.timelineTimer = setInterval(() => {
                        this.timelineIndex = parseInt(this.timelineIndex) + 1;
                        if (this.timelineIndex >= this.economicData.years.length - 1) {
                            clearInterval(this.timelineTimer);
                            this.timelinePlaying = false;
                        }
                    }, 800);
                }
            },
            updateTimelineDisplay() { /* reactive via x-text bindings */ },

            // ===== CORRELATION SCATTER PLOT =====
            updateScatterPlot() {
                const c = this.getChart('scatterChart');
                if (!c) return;
                const d = this.economicData;
                const labels = {
                    gdpGrowth: 'GDP Growth (%)', unemployment: 'Unemployment (%)',
                    top1Share: 'Top 1% Share (%)', formalEmployment: 'Formal Employment (%)',
                    pressFreedom: 'Press Freedom Rank', ssi: 'SSI', fci: 'FCI', dqi: 'DQI',
                    gigWorkers: 'Gig Workers (M)', femaleLFPR: 'Female LFPR (%)'
                };
                const xData = d[this.scatterX];
                const yData = d[this.scatterY];
                if (!xData || !yData) return;

                // Calculate correlation
                const n = xData.length;
                const mx = xData.reduce((a,b) => a+b, 0) / n;
                const my = yData.reduce((a,b) => a+b, 0) / n;
                let num = 0, dx = 0, dy = 0;
                for (let i = 0; i < n; i++) {
                    num += (xData[i] - mx) * (yData[i] - my);
                    dx += (xData[i] - mx) ** 2;
                    dy += (yData[i] - my) ** 2;
                }
                this.correlationR = dx && dy ? num / Math.sqrt(dx * dy) : 0;

                // Build scatter data with year labels
                const scatter = xData.map((x, i) => [x, yData[i], d.years[i]]);

                // Linear regression for trend line
                const slope = dx ? num / dx : 0;
                const intercept = my - slope * mx;
                const xMin = Math.min(...xData);
                const xMax = Math.max(...xData);
                const trendData = [[xMin, slope * xMin + intercept], [xMax, slope * xMax + intercept]];

                const mobile = isMobile();
                c.setOption({
                    ...baseOpts(this.darkMode),
                    title: chartTitle(`${labels[this.scatterX]} vs ${labels[this.scatterY]}`, this.darkMode),
                    tooltip: {
                        formatter: p => {
                            if (p.seriesIndex === 1) return '';
                            return `<strong>${p.data[2]}</strong><br>${labels[this.scatterX]}: ${p.data[0]}<br>${labels[this.scatterY]}: ${p.data[1]}`;
                        }
                    },
                    xAxis: { type: 'value', name: mobile ? '' : labels[this.scatterX], nameLocation: 'center', nameGap: 25, axisLabel: { fontSize: mobile ? 10 : 12 } },
                    yAxis: { type: 'value', name: mobile ? '' : labels[this.scatterY], axisLabel: { fontSize: mobile ? 10 : 12 } },
                    series: [
                        {
                            type: 'scatter', data: scatter, symbolSize: mobile ? 10 : 14,
                            itemStyle: { color: '#8b5cf6', borderColor: '#fff', borderWidth: mobile ? 1 : 2 },
                            label: { show: !mobile, formatter: p => p.data[2], position: 'top', fontSize: 10, color: this.darkMode ? '#94a3b8' : '#6b7280' }
                        },
                        {
                            type: 'line', data: trendData, symbol: 'none',
                            lineStyle: { type: 'dashed', color: '#ef4444', width: 2, opacity: 0.6 },
                            silent: true
                        }
                    ]
                }, true);
            },

            // ===== DATA COVERAGE CHART (Methodology) =====
            createDataCoverageChart() {
                const c = this.getChart('dataCoverageChart');
                if (!c) return;
                const mobile = isMobile();
                c.setOption({
                    ...baseOpts(this.darkMode),
                    title: chartTitle('Data Coverage by Source Type (%)', this.darkMode),
                    tooltip: { trigger: 'axis' },
                    legend: chartLegend(mobile ? ['Govt', 'Independent'] : ['Government Sources', 'Independent Sources']),
                    xAxis: { type: 'category', data: mobile ? ['GDP', 'Emp', 'Ineq', 'Fiscal', 'Dem'] : ['GDP', 'Employment', 'Inequality', 'Fiscal', 'Democratic'], axisLabel: { fontSize: mobile ? 10 : 12 } },
                    yAxis: { type: 'value', max: 100, axisLabel: { formatter: '{value}%' } },
                    series: [
                        { name: 'Government Sources', type: 'bar', data: [100, 85, 60, 95, 30], itemStyle: { color: '#3b82f6' }, barGap: '10%' },
                        { name: 'Independent Sources', type: 'bar', data: [80, 70, 95, 60, 100], itemStyle: { color: '#22c55e' } }
                    ]
                });
            },

            // ===== SSI COMPONENT SANKEY (Methodology) =====
            // Replaces the previous radar. Shows how each component's
            // (severity * weight) contributes to the aggregate SSI score.
            createIndexRadarChart() {
                const c = this.getChart('indexRadarChart');
                if (!c) return;
                const components = [
                    { name: 'Data Suppression',     severity: 100, weight: 30, color: '#ef4444' },
                    { name: 'Release Delays',       severity:  80, weight: 20, color: '#f97316' },
                    { name: 'Institutional Capture',severity:  90, weight: 25, color: '#a855f7' },
                    { name: 'Methodology Changes',  severity:  60, weight: 15, color: '#06b6d4' },
                    { name: 'Access Restrictions',  severity:  70, weight: 10, color: '#10b981' }
                ];
                const target = 'SSI Score';
                const nodes = [...components.map(c => ({ name: c.name, itemStyle: { color: c.color } })),
                               { name: target, itemStyle: { color: '#8b5cf6' } }];
                const links = components.map(c => ({
                    source: c.name,
                    target,
                    value: Math.round((c.severity * c.weight) / 10) / 10
                }));
                c.setOption({
                    ...baseOpts(this.darkMode),
                    title: chartTitle('SSI: How components flow into the score', this.darkMode),
                    tooltip: {
                        trigger: 'item',
                        triggerOn: 'mousemove',
                        formatter: p => p.dataType === 'edge'
                            ? `${p.data.source} → ${p.data.target}<br/>Contribution: <b>${p.data.value}</b>`
                            : `<b>${p.data.name}</b>`
                    },
                    series: [{
                        type: 'sankey',
                        layout: 'none',
                        nodeAlign: 'left',
                        emphasis: { focus: 'adjacency' },
                        data: nodes,
                        links: links,
                        lineStyle: { color: 'gradient', curveness: 0.5, opacity: 0.55 },
                        label: { color: this.darkMode ? '#e2e8f0' : '#1f2937', fontSize: isMobile() ? 10 : 12 }
                    }]
                });
            },

            // ===== DEMOCRATIC DECLINE CHART (Implications) =====
            createDemocraticDeclineChart() {
                const c = this.getChart('democraticDeclineChart');
                if (!c) return;
                const mobile = isMobile();
                c.setOption({
                    ...baseOpts(this.darkMode),
                    title: chartTitle('DQI: Multi-Country Decline (2014-2026)', this.darkMode),
                    tooltip: { trigger: 'axis' },
                    legend: chartLegend(['India', 'Turkey', 'Hungary', 'Brazil']),
                    xAxis: { type: 'category', data: [2014, 2016, 2018, 2020, 2022, 2024, 2026], axisLabel: { fontSize: mobile ? 10 : 12, rotate: mobile ? 45 : 0 } },
                    yAxis: { type: 'value', min: 0.15, max: 0.85, name: mobile ? '' : 'DQI Score', axisLabel: { formatter: v => v.toFixed(2), fontSize: mobile ? 10 : 12 } },
                    dataZoom: dataZoom(),
                    series: [
                        { name: 'India', type: 'line', data: [0.71, 0.68, 0.60, 0.48, 0.43, 0.42, 0.40], smooth: true, itemStyle: { color: '#f97316' }, lineStyle: { width: 3 }, areaStyle: { opacity: 0.08 } },
                        { name: 'Turkey', type: 'line', data: [0.52, 0.45, 0.38, 0.30, 0.22, 0.19, 0.18], smooth: true, itemStyle: { color: '#ef4444' } },
                        { name: 'Hungary', type: 'line', data: [0.63, 0.58, 0.52, 0.48, 0.44, 0.42, 0.41], smooth: true, itemStyle: { color: '#8b5cf6' } },
                        { name: 'Brazil', type: 'line', data: [0.85, 0.82, 0.78, 0.72, 0.68, 0.69, 0.69], smooth: true, itemStyle: { color: '#22c55e' }, lineStyle: { type: 'dashed' } }
                    ],
                    markLine: { data: [{ yAxis: 0.5, label: { formatter: 'Hybrid Regime Threshold', position: 'start' }, lineStyle: { color: '#ef4444', type: 'dashed', opacity: 0.5 } }] }
                });
            },

            // ===== STATE DISPARITIES CHART (Implications) =====
            createStateDisparitiesChart() {
                const c = this.getChart('stateDisparitiesChart');
                if (!c) return;
                const mobile = isMobile();
                const states = mobile
                    ? ['Goa','Delhi','KA','TG','TN','GJ','MH','KL','HR','PB','AP','RJ','WB','OD','CG','JH','MP','UP','Bihar']
                    : ['Goa','Delhi','Karnataka','Telangana','Tamil Nadu','Gujarat','Maharashtra','Kerala','Haryana','Punjab','Andhra Pradesh','Rajasthan','West Bengal','Odisha','Chhattisgarh','Jharkhand','Madhya Pradesh','Uttar Pradesh','Bihar'];
                const gsdp = [575, 450, 320, 305, 290, 275, 270, 260, 255, 210, 195, 140, 130, 115, 105, 95, 90, 75, 55];
                c.setOption({
                    ...baseOpts(this.darkMode),
                    title: chartTitle('Per Capita GSDP by State (₹k, 2025-26)', this.darkMode),
                    tooltip: { trigger: 'axis', formatter: p => `${p[0].name}: ₹${p[0].value}k` },
                    grid: mobile ? { left: 5, right: 10, top: 35, bottom: 5, containLabel: true } : { left: 120, right: 40, top: 40, bottom: 20 },
                    xAxis: { type: 'value', name: '', axisLabel: { formatter: '₹{value}k', fontSize: mobile ? 9 : 12 } },
                    yAxis: { type: 'category', data: states.reverse(), inverse: false, axisLabel: { fontSize: mobile ? 9 : 12 } },
                    series: [{
                        type: 'bar',
                        data: gsdp.reverse().map((v, i) => ({
                            value: v,
                            itemStyle: { color: v > 250 ? '#22c55e' : v > 150 ? '#f59e0b' : v > 100 ? '#f97316' : '#ef4444' }
                        })),
                        barWidth: mobile ? '50%' : '60%',
                        label: { show: !mobile, position: 'right', formatter: '₹{c}k', fontSize: 10 }
                    }],
                    toolbox: { show: false }
                });
            },

            // ===== ERA COMPARISON CHARTS =====
            createEraComparisonChart() {
                const c = this.getChart('eraComparisonChart');
                if (!c) return;
                const mobile = isMobile();
                const indicators = mobile
                    ? ['GDP%', 'Formal\nEmp%', 'Top 1%', 'Unemp%', 'Press\nFreedom']
                    : ['GDP Growth\n(avg %)', 'Formal\nEmployment (%)', 'Top 1%\nShare (%)', 'Unemployment\n(%)', 'Press Freedom\n(rank/180)'];
                const upaValues = [7.4, 13.0, 21.3, 4.9, 140];
                const i = this.latestObservedIndex();
                const ed = this.economicData;
                const gdpAvgNDA = ed.gdpGrowth.slice(0, i + 1).reduce((a, b) => a + b, 0) / (i + 1);
                const ndaValues = [
                    Math.round(gdpAvgNDA * 10) / 10,
                    ed.formalEmployment[i],
                    ed.top1Share[i],
                    ed.unemployment[i],
                    ed.pressFreedom[i]
                ];
                c.setOption({
                    ...baseOpts(this.darkMode),
                    title: chartTitle('UPA (2004-14) vs NDA (2014-26)', this.darkMode),
                    tooltip: { trigger: 'axis' },
                    legend: chartLegend(['UPA Era', 'NDA Era']),
                    xAxis: { type: 'category', data: indicators, axisLabel: { interval: 0, fontSize: mobile ? 9 : 10, lineHeight: mobile ? 12 : 14 } },
                    yAxis: { type: 'value' },
                    series: [
                        { name: 'UPA Era', type: 'bar', data: upaValues, itemStyle: { color: '#3b82f6' }, barGap: '10%' },
                        { name: 'NDA Era', type: 'bar', data: ndaValues, itemStyle: { color: '#f97316' } }
                    ]
                });
            },

            updateEraChart() {
                const c = this.getChart('eraDetailChart');
                if (!c) return;
                const d = this.economicData;
                const labels = {
                    gdpGrowth: 'GDP Growth (%)', unemployment: 'Unemployment (%)',
                    top1Share: 'Top 1% Income Share (%)', formalEmployment: 'Formal Employment (%)',
                    pressFreedom: 'Press Freedom Rank', ssi: 'SSI', dqi: 'DQI'
                };
                const indicator = this.eraIndicator;
                const values = d[indicator];
                if (!values) return;

                // Split into pre-2014 pad + NDA era
                // Since our data starts at 2014, we show the NDA era with a visual midpoint marker
                const midIdx = 0; // 2014 = index 0

                const mobile = isMobile();
                c.setOption({
                    ...baseOpts(this.darkMode),
                    title: chartTitle(`${labels[indicator]}: NDA Era (2014-2026)`, this.darkMode),
                    tooltip: { trigger: 'axis' },
                    xAxis: { type: 'category', data: d.years, axisLabel: { fontSize: mobile ? 10 : 12, rotate: mobile ? 45 : 0 } },
                    yAxis: { type: 'value', name: mobile ? '' : labels[indicator], axisLabel: { fontSize: mobile ? 10 : 12 } },
                    dataZoom: dataZoom(),
                    visualMap: {
                        show: false, dimension: 0, pieces: [
                            { lte: 4, color: '#3b82f6' },  // 2014-2018
                            { gt: 4, color: '#f97316' }     // 2019-2026
                        ]
                    },
                    series: [{
                        type: 'line', data: values, smooth: true,
                        areaStyle: { opacity: 0.12 },
                        markLine: { data: [{ xAxis: '2019', label: { formatter: 'NDA-II', position: 'start' }, lineStyle: { type: 'dashed', color: '#ef4444' } }] }
                    }]
                }, true);
            },

            // ===== SCENARIO LAB =====
            updateScenario() {
                const inp = this.scenarioInputs;
                // Estimated elasticities based on data patterns
                this.scenarioOutputs.ssi = Math.max(0.5, Math.min(10, 10 - (inp.statsReleased / 100) * 9.5));
                this.scenarioOutputs.fci = Math.max(0.3, Math.min(0.95, inp.cessShare / 100 * 3 + 0.19));
                const pressFactor = 1 - (inp.pressFreedom - 30) / 150; // 1.0 at rank 30, 0 at rank 180
                const empFactor = (inp.formalEmp - 8) / 17; // 0 at 8%, 1 at 25%
                const statsFactor = inp.statsReleased / 100;
                this.scenarioOutputs.dqi = Math.max(0.1, Math.min(0.95, (pressFactor * 0.4 + empFactor * 0.2 + statsFactor * 0.4)));

                this.createScenarioChart();
            },

            createScenarioChart() {
                const c = this.getChart('scenarioChart');
                if (!c) return;
                const inp = this.scenarioInputs;
                const out = this.scenarioOutputs;
                // Sankey: levers -> indices, link width = absolute scenario contribution.
                // Mirrors updateScenario() weights so flows reflect the actual model.
                const empFactor    = Math.max(0, Math.min(1, (inp.formalEmp - 8) / 17));
                const pressFactor  = Math.max(0, Math.min(1, 1 - (inp.pressFreedom - 30) / 150));
                const cessFactor   = Math.max(0, Math.min(1, inp.cessShare / 30));
                const statsFactor  = Math.max(0, Math.min(1, inp.statsReleased / 100));
                // Round to one decimal, clamp tiny values to 0.1 so the link is still visible.
                const w = v => Math.max(0.1, Math.round(v * 100) / 100);
                const nodes = [
                    { name: 'Formal Employment',  itemStyle: { color: '#3b82f6' } },
                    { name: 'Press Freedom',      itemStyle: { color: '#a855f7' } },
                    { name: 'Cess Share',         itemStyle: { color: '#f97316' } },
                    { name: 'Statistical Output', itemStyle: { color: '#06b6d4' } },
                    { name: 'SSI (' + out.ssi.toFixed(1) + ')', itemStyle: { color: '#ef4444' } },
                    { name: 'FCI (' + out.fci.toFixed(2) + ')', itemStyle: { color: '#f59e0b' } },
                    { name: 'DQI (' + out.dqi.toFixed(2) + ')', itemStyle: { color: '#22c55e' } }
                ];
                const ssiNode = nodes[4].name, fciNode = nodes[5].name, dqiNode = nodes[6].name;
                const links = [
                    // SSI is driven by statistical output (inverse): the more reports released, the lower SSI.
                    { source: 'Statistical Output', target: ssiNode, value: w(1 - statsFactor + 0.05) },
                    // FCI is driven by cess share (positive).
                    { source: 'Cess Share',         target: fciNode, value: w(cessFactor + 0.1) },
                    // DQI weights from updateScenario(): press 0.4, formalEmp 0.2, statsReleased 0.4
                    { source: 'Press Freedom',      target: dqiNode, value: w(pressFactor * 0.4 + 0.05) },
                    { source: 'Formal Employment', target: dqiNode, value: w(empFactor * 0.2 + 0.05) },
                    { source: 'Statistical Output', target: dqiNode, value: w(statsFactor * 0.4 + 0.05) }
                ];
                c.setOption({
                    ...baseOpts(this.darkMode),
                    title: chartTitle('How your levers flow into the indices', this.darkMode),
                    tooltip: {
                        trigger: 'item',
                        triggerOn: 'mousemove',
                        formatter: p => p.dataType === 'edge'
                            ? `${p.data.source} → ${p.data.target}<br/>Influence: <b>${p.data.value}</b>`
                            : `<b>${p.data.name}</b>`
                    },
                    series: [{
                        type: 'sankey',
                        layout: 'none',
                        nodeAlign: 'left',
                        emphasis: { focus: 'adjacency' },
                        data: nodes,
                        links: links,
                        lineStyle: { color: 'gradient', curveness: 0.5, opacity: 0.55 },
                        label: { color: this.darkMode ? '#e2e8f0' : '#1f2937', fontSize: isMobile() ? 10 : 12 }
                    }]
                }, true);
            },

            // Latest observed (non-projected) index for series lookups
            latestObservedIndex() {
                const yrs = this.economicData.years || [];
                const projStart = (typeof PROJECTION_START_INDEX !== 'undefined') ? PROJECTION_START_INDEX : yrs.length;
                return Math.max(0, Math.min(yrs.length - 1, projStart - 1));
            },
            latestObservedYear() {
                const yrs = this.economicData.years || [];
                return yrs[this.latestObservedIndex()] || '';
            },
            currentRadar() {
                const i = this.latestObservedIndex();
                const d = this.economicData;
                return [d.ssi[i], d.fci[i], d.dqi[i]];
            },
            currentScenarioPreset() {
                const i = this.latestObservedIndex();
                const d = this.economicData;
                return {
                    formalEmp: d.formalEmployment[i],
                    pressFreedom: d.pressFreedom[i],
                    cessShare: 20.5,
                    statsReleased: 40
                };
            },

            applyScenario(preset) {
                const presets = {
                    'optimistic': { formalEmp: 18, pressFreedom: 100, cessShare: 12, statsReleased: 85 },
                    'status-quo': this.currentScenarioPreset(),
                    'pessimistic': { formalEmp: 9, pressFreedom: 175, cessShare: 25, statsReleased: 25 },
                    'nordic': { formalEmp: 22, pressFreedom: 40, cessShare: 8, statsReleased: 98 }
                };
                if (presets[preset]) {
                    this.scenarioInputs = { ...presets[preset] };
                    this.updateScenario();
                }
            },

            // ===== DEEP ANALYSIS =====
            // UPA averages from prior literature (data.json starts at 2014). NDA averages computed live.
            UPA_AVG: {
                gdpGrowth: 7.4, unemployment: 4.9, formalEmployment: 13.0,
                top1Share: 21.3, bottom50Share: 15.0, ssi: 1.8, fci: 0.55,
                dqi: 0.71, pressFreedom: 140
            },
            ndaAverage(key) {
                const i = this.latestObservedIndex();
                const arr = (this.economicData[key] || []).slice(0, i + 1);
                if (!arr.length) return null;
                return arr.reduce((a, b) => a + b, 0) / arr.length;
            },
            fmt(v, dp) {
                if (v === null || v === undefined || Number.isNaN(v)) return '—';
                const f = (typeof dp === 'number') ? v.toFixed(dp) : Math.round(v);
                return f;
            },
            renderRegimeScorecard() {
                const rows = [
                    { key: 'gdpGrowth',          label: 'GDP growth (avg %)',          dp: 1, betterLow: false, suffix: '%' },
                    { key: 'unemployment',       label: 'Unemployment (avg %)',        dp: 1, betterLow: true,  suffix: '%' },
                    { key: 'formalEmployment',   label: 'Formal employment share (%)', dp: 1, betterLow: false, suffix: '%' },
                    { key: 'top1Share',          label: 'Top 1% income share (%)',     dp: 1, betterLow: true,  suffix: '%' },
                    { key: 'bottom50Share',      label: 'Bottom 50% income share (%)', dp: 1, betterLow: false, suffix: '%' },
                    { key: 'ssi',                label: 'Statistical Suppression Idx', dp: 1, betterLow: true,  suffix: '' },
                    { key: 'fci',                label: 'Fiscal Centralization Idx',   dp: 2, betterLow: true,  suffix: '' },
                    { key: 'dqi',                label: 'Democratic Quality Idx',      dp: 2, betterLow: false, suffix: '' },
                    { key: 'pressFreedom',       label: 'Press freedom rank (1-180)',  dp: 0, betterLow: true,  suffix: '' }
                ];
                let html = '';
                for (const r of rows) {
                    const upa = this.UPA_AVG[r.key];
                    const nda = this.ndaAverage(r.key);
                    const change = (nda !== null && upa !== null) ? (nda - upa) : null;
                    const improved = (change !== null) && ((r.betterLow && change < 0) || (!r.betterLow && change > 0));
                    const colour = (change === null || Math.abs(change) < 0.01) ? 'text-gray-500' :
                                   improved ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400';
                    const sign = (change > 0) ? '+' : '';
                    const changeStr = (change === null) ? '—' : sign + this.fmt(change, r.dp) + r.suffix;
                    html += `<tr class="border-b border-gray-100 dark:border-gray-800">
                        <td class="py-2 text-gray-700 dark:text-gray-300">${r.label}</td>
                        <td class="py-2 text-right tabular-nums">${this.fmt(upa, r.dp)}${r.suffix}</td>
                        <td class="py-2 text-right tabular-nums font-semibold">${this.fmt(nda, r.dp)}${r.suffix}</td>
                        <td class="py-2 text-right tabular-nums font-semibold ${colour}">${changeStr}</td>
                    </tr>`;
                }
                return html;
            },
            renderInternationalTable() {
                const d = this.internationalData;
                if (!d || !d.countries) return '';
                let html = '';
                for (let i = 0; i < d.countries.length; i++) {
                    const dV = d.vdem2026[i] - d.vdem2014[i];
                    const dP = d.press2026[i] - d.press2014[i];
                    const vColour = dV > 0 ? 'text-emerald-600 dark:text-emerald-400' : (dV < 0 ? 'text-red-600 dark:text-red-400' : 'text-gray-500');
                    // RSF: lower is better, so a positive delta is worse.
                    const pColour = dP < 0 ? 'text-emerald-600 dark:text-emerald-400' : (dP > 0 ? 'text-red-600 dark:text-red-400' : 'text-gray-500');
                    const isIndia = d.countries[i] === 'India';
                    html += `<tr class="border-b border-gray-100 dark:border-gray-800${isIndia ? ' bg-amber-50/40 dark:bg-amber-900/10' : ''}">
                        <td class="py-2 ${isIndia ? 'font-bold' : 'text-gray-700 dark:text-gray-300'}">${d.countries[i]}</td>
                        <td class="py-2 text-right tabular-nums">${d.vdem2014[i].toFixed(2)}</td>
                        <td class="py-2 text-right tabular-nums font-semibold">${d.vdem2026[i].toFixed(2)}</td>
                        <td class="py-2 text-right tabular-nums font-semibold ${vColour}">${(dV >= 0 ? '+' : '') + dV.toFixed(2)}</td>
                        <td class="py-2 text-right tabular-nums">${d.press2014[i]}</td>
                        <td class="py-2 text-right tabular-nums font-semibold">${d.press2026[i]}</td>
                        <td class="py-2 text-right tabular-nums font-semibold ${pColour}">${dP >= 0 ? '+' : ''}${dP}</td>
                    </tr>`;
                }
                return html;
            },
            renderYoYDeltas() {
                const i = this.latestObservedIndex();
                if (i < 1) return '';
                const d = this.economicData;
                const labels = {
                    gdpGrowth:           ['GDP growth', '%', 1, false],
                    unemployment:        ['Unemployment', '%', 1, true],
                    formalEmployment:    ['Formal emp.', '%', 1, false],
                    top1Share:           ['Top 1% share', '%', 1, true],
                    bottom50Share:       ['Bottom 50% share', '%', 1, false],
                    pressFreedom:        ['Press freedom rank', '', 0, true],
                    ssi:                 ['SSI', '', 1, true],
                    dqi:                 ['DQI', '', 2, false]
                };
                const yLatest = d.years[i];
                const yPrev = d.years[i - 1];
                let html = '';
                for (const key of Object.keys(labels)) {
                    const [label, suffix, dp, betterLow] = labels[key];
                    const arr = d[key]; if (!arr) continue;
                    const cur = arr[i], prev = arr[i - 1];
                    const delta = cur - prev;
                    const improved = (betterLow && delta < 0) || (!betterLow && delta > 0);
                    const colour = Math.abs(delta) < 1e-9 ? 'text-gray-500' :
                                   improved ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400';
                    const sign = delta > 0 ? '+' : '';
                    html += `<div class="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-3">
                        <div class="text-xs text-gray-500 dark:text-gray-400">${label}</div>
                        <div class="text-base font-bold tabular-nums text-gray-900 dark:text-gray-100">${this.fmt(cur, dp)}${suffix}</div>
                        <div class="text-xs tabular-nums ${colour}">${sign}${this.fmt(delta, dp)}${suffix} <span class="text-gray-400">(${yPrev}→${yLatest})</span></div>
                    </div>`;
                }
                return html;
            },
            createDecouplingChart() {
                const c = this.getChart('deepDecouplingChart');
                if (!c) return;
                const d = this.economicData;
                const lastObs = this.latestObservedIndex();
                // Cumulative GDP: compound annual growth from a 2014 base of 100.
                let acc = 100;
                const cumGDP = d.gdpGrowth.map(g => { acc = acc * (1 + g / 100); return Math.round(acc * 10) / 10; });
                const labels = d.yearLabels || d.years.map(String);
                const splitObs = (arr) => arr.map((v, idx) => idx <= lastObs ? v : null);
                const splitProj = (arr) => arr.map((v, idx) => idx >= lastObs ? v : null);
                c.setOption({
                    ...baseOpts(this.darkMode),
                    title: chartTitle('Cumulative GDP (2014=100) vs Formal Employment Share', this.darkMode),
                    tooltip: { trigger: 'axis' },
                    legend: chartLegend(['Cumulative GDP (obs.)', 'Cumulative GDP (proj.)', 'Formal employment % (obs.)', 'Formal employment % (proj.)']),
                    xAxis: { type: 'category', data: labels },
                    yAxis: [
                        { type: 'value', name: 'Cum. GDP (2014=100)', position: 'left' },
                        { type: 'value', name: 'Formal emp. %', position: 'right', min: 8, max: 16 }
                    ],
                    series: [
                        { name: 'Cumulative GDP (obs.)',          type: 'line', data: splitObs(cumGDP),                yAxisIndex: 0, smooth: true, lineStyle: { color: '#3b82f6', width: 2 }, itemStyle: { color: '#3b82f6' }, symbol: 'circle' },
                        { name: 'Cumulative GDP (proj.)',         type: 'line', data: splitProj(cumGDP),               yAxisIndex: 0, smooth: true, lineStyle: { color: '#3b82f6', width: 2, type: 'dashed' }, itemStyle: { color: '#3b82f6' }, symbol: 'emptyCircle' },
                        { name: 'Formal employment % (obs.)',     type: 'line', data: splitObs(d.formalEmployment),    yAxisIndex: 1, smooth: true, lineStyle: { color: '#ef4444', width: 2 }, itemStyle: { color: '#ef4444' }, symbol: 'circle' },
                        { name: 'Formal employment % (proj.)',    type: 'line', data: splitProj(d.formalEmployment),   yAxisIndex: 1, smooth: true, lineStyle: { color: '#ef4444', width: 2, type: 'dashed' }, itemStyle: { color: '#ef4444' }, symbol: 'emptyCircle' }
                    ]
                });
            },

            // ===== SUPPLEMENTARY CSV DATA =====
            csvData: {},
            async loadCSVData() {
                const files = {
                    communal:      'data/society_communal_incidents.csv',
                    incarceration: 'data/politics_opposition_incarceration.csv',
                    education:     'data/education_exam_events.csv',
                    sanitation:    'data/sanitation_odf_verified.csv',
                    cess:          'data/state_finances_cess_share.csv'
                };
                for (const [key, path] of Object.entries(files)) {
                    try {
                        const resp = await fetch(path);
                        if (!resp.ok) continue;
                        const text = await resp.text();
                        const rows = text.trim().split('\n').slice(1).map(line => {
                            const cols = line.split(',');
                            return {
                                year: parseInt(cols[0]),
                                raw: cols[1] ? parseFloat(cols[1]) : null,
                                estimate: parseFloat(cols[2]),
                                lo: parseFloat(cols[3]),
                                hi: parseFloat(cols[4]),
                                method: cols[5] || '',
                                notes: cols.slice(6).join(',') || ''
                            };
                        }).filter(r => !isNaN(r.year));
                        this.csvData[key] = rows;
                    } catch(e) { /* skip silently */ }
                }
            },
            createCSVCharts() {
                const configs = {
                    communal:      { id: 'csvCommunalChart',      title: 'Communal Incidents (reported)',      color: '#ef4444', type: 'line', unit: 'incidents' },
                    incarceration: { id: 'csvIncarcerationChart',  title: 'Opposition Incarceration Cases',    color: '#a855f7', type: 'bar',  unit: 'cases' },
                    education:     { id: 'csvEducationChart',      title: 'Education Exam Disruption Events',  color: '#f97316', type: 'bar',  unit: 'events' },
                    sanitation:    { id: 'csvSanitationChart',     title: 'ODF Verified Coverage (%)',          color: '#22c55e', type: 'line', unit: '%', areaFill: true },
                    cess:          { id: 'csvCessChart',           title: 'Cess/Surcharge Share of Gross Tax Revenue (%)', color: '#3b82f6', type: 'line', unit: '%' }
                };
                for (const [key, cfg] of Object.entries(configs)) {
                    const rows = this.csvData[key];
                    if (!rows || !rows.length) continue;
                    const c = this.getChart(cfg.id);
                    if (!c) continue;
                    const years = rows.map(r => r.year);
                    const est = rows.map(r => r.estimate);
                    const lo = rows.map(r => r.lo);
                    const hi = rows.map(r => r.hi);
                    const series = [];
                    // Confidence band (hi)
                    series.push({
                        name: 'Upper bound',
                        type: 'line', data: hi, stack: 'band',
                        lineStyle: { opacity: 0 }, itemStyle: { opacity: 0 },
                        areaStyle: { color: cfg.color, opacity: 0.08 },
                        symbol: 'none', tooltip: { show: false }
                    });
                    // Confidence band (lo, stacked negative to create gap)
                    series.push({
                        name: 'Lower bound',
                        type: 'line', data: lo, stack: 'band',
                        lineStyle: { opacity: 0 }, itemStyle: { opacity: 0 },
                        areaStyle: { color: '#ffffff', opacity: 1 },
                        symbol: 'none', tooltip: { show: false }
                    });
                    // Main series
                    series.push({
                        name: cfg.title,
                        type: cfg.type === 'bar' ? 'bar' : 'line',
                        data: est, smooth: cfg.type !== 'bar',
                        itemStyle: { color: cfg.color },
                        lineStyle: cfg.type !== 'bar' ? { width: 2.5, color: cfg.color } : undefined,
                        areaStyle: cfg.areaFill ? { color: cfg.color, opacity: 0.12 } : undefined,
                        barWidth: '50%'
                    });
                    c.setOption({
                        ...baseOpts(this.darkMode),
                        title: chartTitle(cfg.title, this.darkMode),
                        tooltip: {
                            trigger: 'axis',
                            formatter: params => {
                                const p = params.find(x => x.seriesName === cfg.title);
                                if (!p) return '';
                                const r = rows[p.dataIndex];
                                return `<b>${r.year}</b><br/>${cfg.title}: <b>${r.estimate}</b> ${cfg.unit}<br/>Range: ${r.lo} – ${r.hi}`;
                            }
                        },
                        xAxis: { type: 'category', data: years, axisLabel: { fontSize: isMobile() ? 10 : 12 } },
                        yAxis: { type: 'value', name: cfg.unit, axisLabel: { fontSize: isMobile() ? 10 : 12 } },
                        series: series
                    });
                }
            },
            exportCSV(key) {
                const rows = this.csvData[key];
                if (!rows || !rows.length) { alert('Data not loaded yet.'); return; }
                let csv = 'year,raw_value,estimate,lo,hi,method,notes\n';
                for (const r of rows) {
                    csv += `${r.year},${r.raw ?? ''},${r.estimate},${r.lo},${r.hi},"${r.method}","${r.notes}"\n`;
                }
                const blob = new Blob([csv], { type: 'text/csv' });
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url; a.download = key + '_data.csv'; a.click();
                URL.revokeObjectURL(url);
            },

            // ===== SHAREABLE CHART SNAPSHOTS =====
            shareChart(chartId) {
                const chart = this.charts[chartId];
                if (!chart) return;
                const url = chart.getDataURL({ type: 'png', pixelRatio: 2, backgroundColor: this.darkMode ? '#1e293b' : '#ffffff' });
                // Create a shareable blob and copy to clipboard
                fetch(url).then(r => r.blob()).then(blob => {
                    if (navigator.clipboard && window.ClipboardItem) {
                        navigator.clipboard.write([new ClipboardItem({ 'image/png': blob })]).then(() => {
                            this.showShareToast('Chart copied to clipboard! Paste anywhere to share.');
                        }).catch(() => {
                            this.fallbackShare(url);
                        });
                    } else {
                        this.fallbackShare(url);
                    }
                });
            },

            fallbackShare(dataUrl) {
                // Fallback: open in new tab
                const w = window.open('');
                if (w) {
                    w.document.write(`<img src="${dataUrl}" style="max-width:100%"><p>Right-click to save or copy this chart.</p>`);
                    w.document.title = 'Some Perspective - Chart Share';
                }
            },

            showShareToast(msg) {
                const toast = document.createElement('div');
                toast.className = 'fixed bottom-6 left-1/2 -translate-x-1/2 bg-green-600 text-white px-6 py-3 rounded-xl shadow-lg z-[100] text-sm font-medium';
                toast.textContent = msg;
                document.body.appendChild(toast);
                setTimeout(() => toast.remove(), 3000);
            }
        };
    }

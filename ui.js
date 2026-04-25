// DOM Elements
const adrSlider = document.getElementById('adrSlider');
const adrValueInput = document.getElementById('adrValue');
const kdSlider = document.getElementById('kdSlider');
const kdValueInput = document.getElementById('kdValue');
const calcBtn = document.getElementById('calcBtn');

// Refined Ranges (Sync with Python)
const ranges = {
    adr: { low: [0, 0, 45, 65], normal: [55, 75, 95], high: [85, 105, 200, 200] },
    kd: { small: [0, 0, 0.7, 1.0], medium: [0.8, 1.1, 1.4], large: [1.2, 1.6, 3.0, 3.0] }
};

// Sync inputs
const syncInput = (slider, input) => {
    slider.addEventListener('input', (e) => {
        input.value = e.target.value;
        updateLiveFuzzification();
    });
    input.addEventListener('change', (e) => {
        slider.value = e.target.value;
        updateLiveFuzzification();
    });
};

syncInput(adrSlider, adrValueInput);
syncInput(kdSlider, kdValueInput);

// Membership Functions (Fixed for edges)
const trapezoid = (x, a, b, c, d) => {
    if (a === b && x <= a) return 1.0;
    if (c === d && x >= c) return 1.0;
    if (x <= a || x >= d) return 0.0;
    if (x >= b && x <= c) return 1.0;
    if (x > a && x < b) return (x - a) / (b - a);
    if (x > c && x < d) return (d - x) / (d - c);
    return 0.0;
};
const triangle = (x, a, b, c) => {
    if (x <= a || x >= c) return 0.0;
    if (x === b) return 1.0;
    if (x > a && x < b) return (x - a) / (b - a);
    if (x > b && x < c) return (c - x) / (c - b);
    return 0.0;
};

function updateLiveFuzzification() {
    const adr = parseFloat(adrSlider.value);
    const kd = parseFloat(kdSlider.value);

    const adrLow = trapezoid(adr, ...ranges.adr.low);
    const adrNormal = triangle(adr, ...ranges.adr.normal);
    const adrHigh = trapezoid(adr, ...ranges.adr.high);

    document.getElementById('adrLow').style.width = (adrLow * 100) + '%';
    document.getElementById('adrLowVal').textContent = adrLow.toFixed(3);
    document.getElementById('adrNormal').style.width = (adrNormal * 100) + '%';
    document.getElementById('adrNormalVal').textContent = adrNormal.toFixed(3);
    document.getElementById('adrHigh').style.width = (adrHigh * 100) + '%';
    document.getElementById('adrHighVal').textContent = adrHigh.toFixed(3);

    const kdSmall = trapezoid(kd, ...ranges.kd.small);
    const kdMedium = triangle(kd, ...ranges.kd.medium);
    const kdLarge = trapezoid(kd, ...ranges.kd.large);

    document.getElementById('kdSmall').style.width = (kdSmall * 100) + '%';
    document.getElementById('kdSmallVal').textContent = kdSmall.toFixed(3);
    document.getElementById('kdMedium').style.width = (kdMedium * 100) + '%';
    document.getElementById('kdMediumVal').textContent = kdMedium.toFixed(3);
    document.getElementById('kdLarge').style.width = (kdLarge * 100) + '%';
    document.getElementById('kdLargeVal').textContent = kdLarge.toFixed(3);
}

// Calculate Action
calcBtn.addEventListener('click', async () => {
    calcBtn.disabled = true;
    calcBtn.textContent = 'Menghitung...';

    const adr = parseFloat(adrSlider.value);
    const kd = parseFloat(kdSlider.value);

    try {
        const response = await fetch('/api/calculate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ adr, kd })
        });
        const data = await response.json();
        updateUI(data);
    } catch (err) {
        console.error(err);
        alert('Gagal menghubungi server Python. Pastikan app.py sudah dijalankan.');
    } finally {
        calcBtn.disabled = false;
        calcBtn.textContent = 'Hitung Rating';
    }
});

function updateUI(data) {
    const rating = data.defuzzification.rating;
    const ringScore = document.getElementById('ringScore');
    const ringProgress = document.getElementById('ringProgress');
    const ringLabel = document.getElementById('ringLabel');
    
    ringScore.textContent = rating || 0;
    const offset = 364 - (rating / 100) * 364;
    ringProgress.style.strokeDashoffset = offset;

    const badgeTitle = document.getElementById('badgeTitle');
    const badgeMedal = document.getElementById('badgeMedal');
    
    let color = '#8B4513';
    if (rating >= 85) { badgeTitle.textContent = 'MVP'; badgeMedal.textContent = '⭐'; color = '#ff6b35'; }
    else if (rating >= 65) { badgeTitle.textContent = 'GOLD'; badgeMedal.textContent = '🥇'; color = '#f0b429'; }
    else if (rating >= 45) { badgeTitle.textContent = 'SILVER'; badgeMedal.textContent = '🥈'; color = '#9e9e9e'; }
    else { badgeTitle.textContent = 'BRONZE'; badgeMedal.textContent = '🥉'; color = '#8B4513'; }
    
    ringLabel.textContent = badgeTitle.textContent;
    ringScore.style.color = color;
    ringProgress.style.stroke = color;

    const aggr = data.aggregation;
    document.getElementById('outBronze').style.width = (aggr.Bronze * 100) + '%';
    document.getElementById('outBronzeVal').textContent = aggr.Bronze.toFixed(3);
    document.getElementById('outSilver').style.width = (aggr.Silver * 100) + '%';
    document.getElementById('outSilverVal').textContent = aggr.Silver.toFixed(3);
    document.getElementById('outGold').style.width = (aggr.Gold * 100) + '%';
    document.getElementById('outGoldVal').textContent = aggr.Gold.toFixed(3);
    document.getElementById('outMVP').style.width = (aggr.MVP * 100) + '%';
    document.getElementById('outMVPVal').textContent = aggr.MVP.toFixed(3);
}



window.onload = () => {
    updateLiveFuzzification();
};

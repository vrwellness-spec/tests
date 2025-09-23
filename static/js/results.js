
document.addEventListener('DOMContentLoaded', () => {
    const resultsBreakdown = document.getElementById('results-breakdown');
    const validityDetails = document.getElementById('validity-details');
    const detailedReportTableBody = document.querySelector('#detailed-report-table tbody');
    const sessionId = window.location.pathname.split('/').pop();

    const SCALE_NAMES = {
        'X': 'Disclosure',
        'Y': 'Desirability',
        'Z': 'Debasement',
        '1': 'Schizoid',
        '2A': 'Avoidant',
        '2B': 'Depressive',
        '3': 'Dependent',
        '4': 'Histrionic',
        '5': 'Narcissistic',
        '6A': 'Antisocial',
        '6B': 'Sadistic/Aggressive',
        '7': 'Compulsive',
        '8A': 'Negativistic/Passive-Aggressive',
        '8B': 'Masochistic/Self-Defeating',
        'S': 'Schizotypal',
        'C': 'Borderline',
        'P': 'Paranoid',
        'A': 'Anxiety',
        'H': 'Somatoform',
        'N': 'Bipolar: Manic',
        'D': 'Dysthymia',
        'B': 'Alcohol Dependence',
        'T': 'Drug Dependence',
        'R': 'Post-Traumatic Stress Disorder',
        'SS': 'Thought Disorder',
        'CC': 'Major Depression',
        'PP': 'Delusional Disorder'
    };

    const CATEGORIES = {
        'Modifying Indices': ['X', 'Y', 'Z'],
        'Clinical Personality Patterns': ['1', '2A', '2B', '3', '4', '5', '6A', '6B', '7', '8A', '8B'],
        'Severe Personality Pathology': ['S', 'C', 'P'],
        'Clinical Syndromes': ['A', 'H', 'N', 'D', 'B', 'T', 'R'],
        'Severe Clinical Syndromes': ['SS', 'CC', 'PP']
    };

    async function fetchResults() {
        try {
            const response = await fetch(`/api/results/${sessionId}`);
            if (!response.ok) {
                throw new Error('Failed to fetch results.');
            }
            const data = await response.json();
            renderValidityReport(data.validity_report);
            renderDetailedReport(data.detailed_breakdown, data.ad_summary);
            renderGraphicalReport(data.detailed_breakdown);
        } catch (error) {
            resultsBreakdown.innerHTML = `<p>Error loading results: ${error.message}</p>`;
        }
    }

    function renderValidityReport(report) {
        if (!report) {
            validityDetails.innerHTML = "<p>Validity assessment not available for this report.</p>";
            return;
        }

        let interpretationsHtml = '<ul>';
        report.interpretations.forEach(interp => {
            interpretationsHtml += `<li>${interp}</li>`;
        });
        interpretationsHtml += '</ul>';

        validityDetails.innerHTML = `
            <p><strong>Overall Validity:</strong> <span class="validity-${report.overall_validity.split(' ')[0].toLowerCase()}">${report.overall_validity}</span></p>
            <p><strong>Scale V (Invalidity):</strong> ${report.scale_v_raw}</p>
            <p><strong>Scale W (Inconsistency):</strong> ${report.scale_w_raw}</p>
            <h4>Interpretations:</h4>
            ${interpretationsHtml}
        `;
    }

    function renderDetailedReport(detailedBreakdown, adSummary) {
        if (!detailedBreakdown) return;
        
        detailedReportTableBody.innerHTML = '';
        
        // Add A/D adjustment summary information above the table
        if (adSummary && adSummary.adjusted_scales.length > 0) {
            const summaryRow = document.createElement('tr');
            summaryRow.style.backgroundColor = '#f0f8ff';
            summaryRow.innerHTML = `
                <td colspan="7" style="text-align: center; padding: 10px; font-weight: bold;">
                    <div>A/D Adjustment: ${adSummary.ad_calculation}</div>
                    <div style="font-size: 0.9em; margin-top: 5px;">${adSummary.adjustment_reason}</div>
                </td>
            `;
            detailedReportTableBody.appendChild(summaryRow);
        }
        
        // Create a custom order that matches the graphical display categories
        const scaleOrder = [
            // Modifying Indices
            'X', 'Y', 'Z',
            // Clinical Personality Patterns
            '1', '2A', '2B', '3', '4', '5', '6A', '6B', '7', '8A', '8B',
            // Severe Personality Pathology
            'S', 'C', 'P',
            // Clinical Syndromes
            'A', 'H', 'N', 'D', 'B', 'T', 'R',
            // Severe Clinical Syndromes
            'SS', 'CC', 'PP'
        ];
        
        // Define which scales get 1-8B adjustment (left aligned) vs S-PP adjustment (right aligned)
        const personalityPatternScales = ['1', '2A', '2B', '3', '4', '5', '6A', '6B', '7', '8A', '8B'];
        const sppAdjustmentScales = ['S', 'C', 'P', 'A', 'H', 'N', 'D', 'B', 'T', 'R', 'SS', 'CC', 'PP'];
        
        // Sort the detailed breakdown according to the scale order
        const sortedBreakdown = detailedBreakdown.sort((a, b) => {
            const indexA = scaleOrder.indexOf(a.scale);
            const indexB = scaleOrder.indexOf(b.scale);
            return indexA - indexB;
        });
        
        sortedBreakdown.forEach(item => {
            const row = document.createElement('tr');
            
            // Determine alignment for disclosure adjustment column
            let disclosureAdjDisplay = '';
            if (personalityPatternScales.includes(item.scale)) {
                // Left aligned for 1-8B scales (get 1st-BR adjustment)
                disclosureAdjDisplay = `<span style="text-align: left; display: block;">${item.disclosure_adj}</span>`;
            } else if (sppAdjustmentScales.includes(item.scale)) {
                // Right aligned for S-PP adjustment scales
                disclosureAdjDisplay = `<span style="text-align: right; display: block;">${item.disclosure_adj}</span>`;
            } else {
                // Center aligned for scales with no disclosure adjustment (modifying indices)
                disclosureAdjDisplay = `<span style="text-align: center; display: block;">${item.disclosure_adj}</span>`;
            }
            
            row.innerHTML = `
                <td><strong>${item.scale}</strong> - ${SCALE_NAMES[item.scale] || ''}</td>
                <td>${item.raw}</td>
                <td>${item.br}</td>
                <td>${disclosureAdjDisplay}</td>
                <td>${item.ad_adj}</td>
                <td>${item.dc_adj}</td>
                <td><strong>${item.final}</strong></td>
            `;
            detailedReportTableBody.appendChild(row);
        });
    }

    function renderGraphicalReport(detailedBreakdown) {
        if (!detailedBreakdown) return;
        resultsBreakdown.innerHTML = ''; // Clear previous content

        for (const categoryName in CATEGORIES) {
            const categoryScales = CATEGORIES[categoryName];
            const categoryElement = document.createElement('div');
            categoryElement.classList.add('scale-category');
            
            let categoryHtml = `<h2>${categoryName} (Graphical)</h2>`;

            for (const scaleCode of categoryScales) {
                const scoreData = detailedBreakdown.find(item => item.scale === scaleCode);
                if (scoreData) {
                    const finalScore = scoreData.final;
                    const scaleName = SCALE_NAMES[scaleCode];
                    
                    let barColor = 'green';
                    if (finalScore >= 85) {
                        barColor = 'red';
                    } else if (finalScore >= 75) {
                        barColor = 'yellow';
                    }

                    categoryHtml += `
                        <div class="scale">
                            <div class="scale-info">
                                <strong>${scaleCode} - ${scaleName}</strong><br>
                                Final BR: ${finalScore}
                            </div>
                            <div class="scale-chart">
                                <div class="bar ${barColor}" style="width: ${(finalScore / 115) * 100}%;"></div>
                                <div class="marker" style="left: ${(60 / 115) * 100}%;"></div>
                                <div class="marker" style="left: ${(75 / 115) * 100}%;"></div>
                                <div class="marker" style="left: ${(85 / 115) * 100}%;"></div>
                            </div>
                        </div>
                    `;
                }
            }
            categoryElement.innerHTML = categoryHtml;
            resultsBreakdown.appendChild(categoryElement);
        }
    }

    // Print functionality
    function setupPrintButtons() {
        const printPdfBtn = document.getElementById('print-pdf-btn');
        const printWordBtn = document.getElementById('print-word-btn');
        
        if (printPdfBtn) {
            printPdfBtn.addEventListener('click', async () => {
                const sessionId = window.location.pathname.split('/').pop();
                
                // Disable button and show loading
                printPdfBtn.disabled = true;
                printPdfBtn.textContent = 'Generating PDF...';
                
                try {
                    const response = await fetch(`/api/print-pdf/${sessionId}`);
                    
                    if (response.ok) {
                        // Create blob and download
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `assessment_results_${sessionId}.pdf`;
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        window.URL.revokeObjectURL(url);
                    } else {
                        const error = await response.json();
                        alert(`Error generating PDF: ${error.error}`);
                    }
                } catch (error) {
                    alert(`Error: ${error.message}`);
                } finally {
                    // Re-enable button
                    printPdfBtn.disabled = false;
                    printPdfBtn.textContent = '📊 Print PDF Graph';
                }
            });
        }
        
        if (printWordBtn) {
            printWordBtn.addEventListener('click', async () => {
                const sessionId = window.location.pathname.split('/').pop();
                
                // Disable button and show loading
                printWordBtn.disabled = true;
                printWordBtn.textContent = 'Generating Report...';
                
                try {
                    const response = await fetch(`/api/print-word/${sessionId}`);
                    
                    if (response.ok) {
                        // Create blob and download
                        const blob = await response.blob();
                        const url = window.URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `assessment_report_${sessionId}.docx`;
                        document.body.appendChild(a);
                        a.click();
                        document.body.removeChild(a);
                        window.URL.revokeObjectURL(url);
                    } else {
                        const error = await response.json();
                        alert(`Error generating Word report: ${error.error}`);
                    }
                } catch (error) {
                    alert(`Error: ${error.message}`);
                } finally {
                    // Re-enable button
                    printWordBtn.disabled = false;
                    printWordBtn.textContent = '📄 Generate Word Report';
                }
            });
        }
    }

    fetchResults();
    setupPrintButtons();
});

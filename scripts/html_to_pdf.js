const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  try {
    const browser = await puppeteer.launch({
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    const page = await browser.newPage();

    const htmlPath = path.resolve('paper.html');
    const fileUrl = 'file://' + htmlPath;

    console.log(`Loading ${fileUrl}...`);
    await page.goto(fileUrl, {
      waitUntil: 'networkidle0'
    });

    console.log('Injecting Eisvogel-like styles...');
    await page.addStyleTag({
      content: `
        @page {
          size: letter;
          margin: 1in;
        }
        body {
          font-family: "DejaVu Serif", serif;
          line-height: 1.5;
          font-size: 11pt;
          color: #1a1a1a;
          max-width: 100%;
          margin: 0;
          padding: 0;
        }
        h1, h2, h3, h4, h5, h6 {
          font-family: "DejaVu Sans", sans-serif;
          color: #003366;
          margin-top: 1.5em;
          margin-bottom: 0.5em;
        }
        h1 { font-size: 24pt; border-bottom: 2px solid #003366; padding-bottom: 0.2em; }
        h2 { font-size: 18pt; }
        h3 { font-size: 14pt; }

        a { color: #0066cc; text-decoration: none; }

        code {
          font-family: "DejaVu Sans Mono", monospace;
          background-color: #f4f4f4;
          padding: 0.2em 0.4em;
          border-radius: 3px;
          font-size: 85%;
        }
        pre {
          background-color: #f4f4f4;
          padding: 1em;
          border-left: 5px solid #ccc;
          overflow-x: auto;
          margin: 1.5em 0;
        }
        pre code { background-color: transparent; padding: 0; }

        table {
          border-collapse: collapse;
          width: 100%;
          margin: 1.5em 0;
        }
        th, td {
          border: 1px solid #ddd;
          padding: 8px;
          text-align: left;
        }
        th {
          background-color: #f2f2f2;
          font-family: "DejaVu Sans", sans-serif;
        }

        img {
          max-width: 100%;
          height: auto;
          display: block;
          margin: 2em auto;
          box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .caption {
          text-align: center;
          font-style: italic;
          font-size: 10pt;
          margin-top: -1.5em;
          margin-bottom: 2em;
          color: #555;
        }

        /* Table of contents styling */
        #TOC {
          background: #f9f9f9;
          padding: 1.5em;
          border: 1px solid #eee;
          margin-bottom: 3em;
        }
        #TOC ul { list-style: none; padding-left: 1.5em; }
        #TOC > ul { padding-left: 0; }
        #TOC a { color: #333; }
        #TOC a:hover { color: #0066cc; }
      `
    });

    console.log('Generating PDF...');
    await page.pdf({
      path: 'paper.pdf',
      format: 'Letter',
      printBackground: true,
      displayHeaderFooter: true,
      headerTemplate: '<div style="font-size: 9pt; width: 100%; text-align: center; color: #999;">Healthcare Analytics Challenges - January 2026</div>',
      footerTemplate: '<div style="font-size: 9pt; width: 100%; text-align: center; color: #999;"><span class="pageNumber"></span> / <span class="totalPages"></span></div>',
      margin: {
        top: '1.2in',
        bottom: '1in',
        left: '1in',
        right: '1in'
      }
    });

    await browser.close();
    console.log('Successfully generated paper.pdf');
  } catch (error) {
    console.error('Error generating PDF:', error);
    process.exit(1);
  }
})();

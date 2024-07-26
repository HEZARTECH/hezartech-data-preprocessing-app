/*
* This javascript file is for Label Editor functionality and utilities.
*/

let currentTag = '';
let currentPage = 1;
let selected_tag_btn = document.getElementById('selected-tag-btn')
let totalPages = document.querySelectorAll('.text-page').length;
const pageInput = document.getElementById('pageInput')
const filename = document.getElementById('filename').textContent;

let tag_colors = {
    "FIRMA": "3b82f6",
    "POZITIF": "10b981",
    "NOTR": "6b7280",
    "NEGATIF": "ef4444",
    "YOK!": "6b7280"
}

function setTag(tag) {
    currentTag = tag;
    if(tag === '') {
        selected_tag_btn.innerText = 'Seçili Tag: YOK!';
        selected_tag_btn.style.backgroundColor = "#6b7280";
        return;
    }
    selected_tag_btn.innerText = 'Seçili Tag: ' + tag;
    selected_tag_btn.style.backgroundColor = "#" + tag_colors[tag];
}

  const bodyElement = document.querySelector('body');

function listen_keyboard(event) {
    let key = event.key;
    if(key == "1")
    {
        setTag('FIRMA');
    }
    if(key == "2")
    {
        setTag('POZITIF');
    }
    if(key == "3")
    {
        setTag('NOTR');
    }
    if(key == "4")
    {
        setTag('NEGATIF');
    }
    if(key == "d" || key == "D")
    {
        deletePage();
    }
    if(key == "r" || key == "R")
    {
        setTag('');
    }
    if(event.keyCode == "37") // Left arrow
    {
        prevPage();
    }
    if(event.keyCode == "39") // Right arrow
    {
        nextPage();
    }
    if(key == "q")
    {
        prevPage();
    }
    if(key == "e")
    {
        nextPage();
    }
  }

bodyElement.onkeydown = listen_keyboard;

function resetForCurrentPage() {
    const selectedSpans = document.querySelectorAll('.selected');

    selectedSpans.forEach(span => {
        spanPage = parseInt(span.getAttribute('data-page'))

        if (currentPage == spanPage){
            const text = span.textContent;
            const parent = span.parentElement;

            parent.replaceChild(document.createTextNode(text), span);
        }
    });
}

document.getElementById('text-container').addEventListener('mouseup', function () {
    const selection = window.getSelection();
    if (selection.toString().length > 0 && currentTag) {
    const range = selection.getRangeAt(0);
    const span = document.createElement('span');
    span.className = `selected tag-${currentTag.toLowerCase()} selectable`;
    span.textContent = selection.toString();
    span.dataset.tag = currentTag;
    span.dataset.page = currentPage;
    range.surroundContents(span);
    selection.removeAllRanges();
    }
});

function exportSelectedDataAsJSON() {
    const selectedData = getSelectedData();
    const exportObj = {
        dataset: filename,
        data: selectedData
    }
    const jsonData = JSON.stringify(exportObj, null, 2);
    const downloadLink = document.createElement('a');
    downloadLink.href = 'data:text/json;charset=utf-8,' + encodeURIComponent(jsonData);
    downloadLink.download = 'labeled_dataset.json';
    document.body.appendChild(downloadLink);
    downloadLink.click();
    document.body.removeChild(downloadLink);

    fetch('/exportData/json', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body: jsonData
    })
    .then(response => response.text())
    .then(data => {
        console.log('Success:', data.success);
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}



function getSelectedData() {
    const pages = document.querySelectorAll('.text-page');
    const selectedData = Array.from(pages).map(page => {
        const pageId = page.dataset.page;
        const pageText = page.textContent.trim();
        const selectedSpans = page.querySelectorAll('.selected');
        const annotations = Array.from(selectedSpans).map(span => {
            const text = span.textContent;
            const tag = span.dataset.tag;
            const startOffset = pageText.indexOf(text);
            const endOffset = startOffset + text.length;

            return {
            tag: tag,
            start: startOffset,
            end: endOffset,
            text: text
            };
        });

        return {
            page: pageId,
            text: pageText,
            annotations: annotations
        };
    });

    return selectedData;
}

function gotoPage() {
const pageInput = document.getElementById('pageInput');
const pageNumber = parseInt(pageInput.value);

if (!isNaN(pageNumber) && pageNumber >= 1 && pageNumber <= totalPages) {
    currentPage = pageNumber
    showPage(pageNumber);
} else {
    alert(`Lütfen 1 ile ${totalPages} arasında bir değer girin.`);
}
pageInput.value = currentPage; // Clear input field after navigation
}

function showPage(page) {
    document.querySelectorAll('.text-page').forEach((el, index) => {
        el.classList.toggle('hidden', index !== page - 1);
    });
    updateProgressBar();
}

function nextPage() {
    if (currentPage < totalPages) {
        currentPage++;
        showPage(currentPage);
        pageInput.value = currentPage;
    }
}

function prevPage() {
    if (currentPage > 1) {
        currentPage--;
        showPage(currentPage);
        pageInput.value = currentPage;
    }
}

function updateProgressBar() {
  const progress = (currentPage / totalPages) * 100;
  const progressBar = document.getElementById('progress-bar');
  const progressText = document.getElementById('progress-text');
  progressBar.style.width = `${progress}%`;
  progressText.textContent = `Sayfa ${currentPage} / ${totalPages}`;
}

function deletePage() {
  if (totalPages > 1) {
    const pageToDelete = document.getElementById(`page-${currentPage}`);
    pageToDelete.parentNode.removeChild(pageToDelete);

    // Update the IDs and data-page attributes of the remaining pages
    const pages = document.querySelectorAll('.text-page');
    pages.forEach((page, index) => {
      page.id = `page-${index + 1}`;
      page.dataset.page = index + 1;
    });

    totalPages = totalPages-1;
    if (currentPage > totalPages) {
      currentPage = totalPages;
    }
    showPage(currentPage);
    updateProgressBar();
  } else {
    alert("Son kalan sayfayı silemezsin.");
  }
}


showPage(currentPage);
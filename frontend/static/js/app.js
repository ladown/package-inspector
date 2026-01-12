document.addEventListener('DOMContentLoaded', () => {
    let referenceFile = null;
    let testFile = null;

    const referenceInput = document.querySelector('#reference-input');
    const testInput = document.querySelector('#test-input');
    const compareButton = document.querySelector('#compare-btn');
    const resultsContainer = document.querySelector('#results');
    const statusBadge = document.querySelector('#status-badge');
    const similarityElement = document.querySelector('#similarity');
    const defectsCountElement = document.querySelector('#defects-count');
    const annotatedContainer = document.querySelector('#annotated-container');
    const annotatedImage = document.querySelector('#annotated-image');
    const loadingElement = document.querySelector('#loading');
    const errorContainer = document.querySelector('#error');

    const handleFileSelect = (event, imageType) => {
        const selectedFile = event.target.files[0];
        if (!selectedFile) return;

        if (imageType === 'reference') {
            referenceFile = selectedFile;
        } else {
            testFile = selectedFile;
        }

        const fileReader = new FileReader();
        fileReader.onload = (readerEvent) => {
            const previewId = imageType === 'reference' ? 'reference-preview' : 'test-preview';
            const previewElement = document.querySelector(`#${previewId}`);
            previewElement.innerHTML = `<img src="${readerEvent.target.result}" alt="${imageType}" class="max-w-full h-auto rounded-lg shadow">`;
        };
        fileReader.readAsDataURL(selectedFile);

        updateCompareButton();
    };

    const updateCompareButton = () => {
        compareButton.disabled = !(referenceFile && testFile);
    };

    const compareImages = async () => {
        hideError();
        showLoading(true);
        resultsContainer.classList.add('hidden');

        const formData = new FormData();
        formData.append('reference', referenceFile);
        formData.append('test', testFile);

        try {
            const response = await fetch('/api/compare', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || 'Ошибка при сравнении изображений');
            }

            const comparisonResult = await response.json();
            displayResults(comparisonResult);
        } catch (error) {
            showError(error.message);
        } finally {
            showLoading(false);
        }
    };

    const displayResults = (comparisonResult) => {
        resultsContainer.classList.remove('hidden');

        if (comparisonResult.status === 'OK') {
            statusBadge.className = 'inline-block px-6 py-3 bg-green-500 text-white text-lg font-bold rounded-lg';
            statusBadge.textContent = 'ВСЕ ЭЛЕМЕНТЫ НА МЕСТЕ';
        } else {
            statusBadge.className = 'inline-block px-6 py-3 bg-red-500 text-white text-lg font-bold rounded-lg';
            statusBadge.textContent = 'ОБНАРУЖЕНЫ ОТКЛОНЕНИЯ';
        }

        similarityElement.textContent = (comparisonResult.similarity_score * 100).toFixed(1) + '%';
        defectsCountElement.textContent = comparisonResult.defects_count;

        if (comparisonResult.status === 'FAIL' && comparisonResult.annotated_image) {
            annotatedImage.src = comparisonResult.annotated_image;
            annotatedContainer.classList.remove('hidden');
        } else {
            annotatedContainer.classList.add('hidden');
        }
    };

    const showLoading = (isLoading) => {
        loadingElement.classList.toggle('hidden', !isLoading);
        compareButton.disabled = isLoading;
    };

    const showError = (errorMessage) => {
        errorContainer.textContent = errorMessage;
        errorContainer.classList.remove('hidden');
    };

    const hideError = () => {
        errorContainer.classList.add('hidden');
    };

    referenceInput.addEventListener('change', (event) => handleFileSelect(event, 'reference'));
    testInput.addEventListener('change', (event) => handleFileSelect(event, 'test'));
    compareButton.addEventListener('click', compareImages);
});

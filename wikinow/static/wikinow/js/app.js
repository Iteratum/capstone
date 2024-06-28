document.addEventListener('DOMContentLoaded', () => {
  const toggleSwitch = document.getElementById('toggle-switch');
  const searchForm = document.getElementById('search-form');
  const wikiSearchForm = document.getElementById('wiki-search-form');
  const searchInput = document.getElementById('search-input');
  const wikiSearchInput = document.getElementById('wiki-search-input');
  const suggestionsContainer = document.getElementById('suggestions');
  const wikiSuggestionsContainer = document.getElementById('wiki-suggestions');
  const toggleTooltip = document.getElementById('toggle-tooltip');
  const infoModal = document.getElementById('info-modal');
  const closeModal = document.getElementById('close-modal');

  // Show modal on page load if not previously displayed
  if (!sessionStorage.getItem('modalDisplayed')) {
      infoModal.classList.remove('hidden');
  }

  closeModal.addEventListener('click', () => {
      infoModal.classList.add('hidden');
      // Set modal displayed flag in session storage
      sessionStorage.setItem('modalDisplayed', 'true');
  });

  // Reset the toggle switch and forms' visibility state on page load
  toggleSwitch.checked = false;
  searchForm.classList.remove('hidden');
  wikiSearchForm.classList.add('hidden');

  toggleSwitch.addEventListener('change', () => {
      if (toggleSwitch.checked) {
          searchForm.classList.add('hidden');
          wikiSearchForm.classList.remove('hidden');
      } else {
          searchForm.classList.remove('hidden');
          wikiSearchForm.classList.add('hidden');
      }
  });

  searchForm.addEventListener('submit', (event) => {
      event.preventDefault();
  });

  wikiSearchForm.addEventListener('submit', (event) => {
      event.preventDefault();
  });

  searchInput.addEventListener('input', () => {
      const query = searchInput.value;
      if (query.length > 1) {
          fetch(`/search/?q=${query}`)
              .then(response => response.json())
              .then(data => {
                  suggestionsContainer.innerHTML = '';
                  if (data.length > 0) {
                      suggestionsContainer.classList.remove('hidden');
                      data.forEach(item => {
                          const suggestionItem = document.createElement('a');
                          suggestionItem.href = `/view_page/${item.id}`;
                          suggestionItem.classList.add('block', 'p-2', 'hover:bg-gray-200');
                          suggestionItem.textContent = item.title;
                          suggestionsContainer.appendChild(suggestionItem);
                      });
                  } else {
                      suggestionsContainer.innerHTML = '<div class="block p-2">Search not found</div>';
                      suggestionsContainer.classList.remove('hidden');
                  }
              });
      } else {
          suggestionsContainer.classList.add('hidden');
          suggestionsContainer.innerHTML = '';
      }
  });

  wikiSearchInput.addEventListener('input', () => {
      const query = wikiSearchInput.value;
      if (query.length > 1) {
          fetch(`https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=${query}&format=json&origin=*`)
              .then(response => response.json())
              .then(data => {
                  wikiSuggestionsContainer.innerHTML = '';
                  if (data.query.search.length > 0) {
                      wikiSuggestionsContainer.classList.remove('hidden');
                      data.query.search.forEach(item => {
                          const suggestionItem = document.createElement('a');
                          suggestionItem.href = `https://en.wikipedia.org/wiki/${item.title}`;
                          suggestionItem.target = '_blank';
                          suggestionItem.classList.add('block', 'p-2', 'hover:bg-gray-200');
                          suggestionItem.textContent = item.title;
                          wikiSuggestionsContainer.appendChild(suggestionItem);
                      });
                  } else {
                      wikiSuggestionsContainer.innerHTML = '<div class="block p-2">Search not found</div>';
                      wikiSuggestionsContainer.classList.remove('hidden');
                  }
              });
      } else {
          wikiSuggestionsContainer.classList.add('hidden');
          wikiSuggestionsContainer.innerHTML = '';
      }
  });

  document.addEventListener('click', (event) => {
      if (!searchInput.contains(event.target) && !suggestionsContainer.contains(event.target)) {
          suggestionsContainer.classList.add('hidden');
      }
      if (!wikiSearchInput.contains(event.target) && !wikiSuggestionsContainer.contains(event.target)) {
          wikiSuggestionsContainer.classList.add('hidden');
      }
  });

  toggleSwitch.addEventListener('mouseenter', () => {
      toggleTooltip.classList.remove('hidden');
  });

  toggleSwitch.addEventListener('mouseleave', () => {
      toggleTooltip.classList.add('hidden');
  });
});
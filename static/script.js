// Inicializace při načtení stránky
document.addEventListener('DOMContentLoaded', () => {
    loadPeople();
    
    // Enter pro přidání člověka
    document.getElementById('personInput').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            addPerson();
        }
    });
    
    // Zavření modálu kliknutím mimo něj
    document.getElementById('addPersonModal').addEventListener('click', (e) => {
        if (e.target.id === 'addPersonModal') {
            closeAddPersonModal();
        }
    });
});

// Otevření modálního okna
function openAddPersonModal() {
    const modal = document.getElementById('addPersonModal');
    modal.classList.add('active');
    document.getElementById('personInput').focus();
    document.getElementById('error-message').textContent = '';
}

// Zavření modálního okna
function closeAddPersonModal() {
    const modal = document.getElementById('addPersonModal');
    modal.classList.remove('active');
    document.getElementById('personInput').value = '';
    document.getElementById('error-message').textContent = '';
}

// Načtení seznamu lidí
async function loadPeople() {
    try {
        const response = await fetch('/api/people');
        const people = await response.json();
        
        const peopleList = document.getElementById('people-list');
        
        if (people.length === 0) {
            peopleList.innerHTML = '<p class="empty-state">Zatím tu nikdo není. Přidej prvního člověka!</p>';
            return;
        }
        
        // Seřaď lidi podle bodů (sestupně)
        people.sort((a, b) => b.points - a.points);
        
        peopleList.innerHTML = people.map(person => `
            <div class="person-card">
                <div class="person-header">
                    <span class="person-name">${escapeHtml(person.name)}</span>
                    <span class="person-points">${person.points} bodů</span>
                </div>
                <div class="person-controls">
                    <button class="btn-small btn-add" onclick="addPoint(${person.id})">+1 bod</button>
                    <button class="btn-small btn-subtract" onclick="removePoint(${person.id})">-1 bod</button>
                    <button class="btn-small btn-delete" onclick="deletePerson(${person.id})">Smazat</button>
                </div>
            </div>
        `).join('');
        
    } catch (error) {
        console.error('Chyba při načítání lidí:', error);
    }
}

// Přidání nového člověka
async function addPerson() {
    const input = document.getElementById('personInput');
    const name = input.value.trim();
    const errorMsg = document.getElementById('error-message');
    
    errorMsg.textContent = '';
    
    if (!name) {
        errorMsg.textContent = 'Prosím, zadej jméno!';
        return;
    }
    
    const password = getPassword();
    if (!password) {
        errorMsg.textContent = 'Heslo je povinné!';
        return;
    }
    
    try {
        const response = await fetch('/api/people', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name: name, password: password })
        });
        
        if (response.ok) {
            input.value = '';
            closeAddPersonModal();
            loadPeople();
        } else {
            const error = await response.json();
            errorMsg.textContent = error.error || 'Chyba při přidávání člověka';
        }
    } catch (error) {
        console.error('Chyba:', error);
        errorMsg.textContent = 'Chyba při komunikaci se serverem';
    }
}

// Přidání bodu
async function addPoint(personId) {
    const password = getPassword();
    if (!password) {
        return;
    }
    
    try {
        const response = await fetch(`/api/people/${personId}/points`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ change: 1, password: password })
        });
        
        if (response.ok) {
            loadPeople();
        } else {
            const error = await response.json();
            alert(error.error || 'Chyba při aktualizaci bodů');
        }
    } catch (error) {
        console.error('Chyba:', error);
    }
}

// Odstranění bodu
async function removePoint(personId) {
    const password = getPassword();
    if (!password) {
        return;
    }
    
    try {
        const response = await fetch(`/api/people/${personId}/points`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ change: -1, password: password })
        });
        
        if (response.ok) {
            loadPeople();
        } else {
            const error = await response.json();
            alert(error.error || 'Chyba při aktualizaci bodů');
        }
    } catch (error) {
        console.error('Chyba:', error);
    }
}

// Smazání člověka
async function deletePerson(personId) {
    if (!confirm('Opravdu chceš smazat tohoto člověka?')) {
        return;
    }
    const password = getPassword();
    if (!password) {
        return;
    }
    
    try {
        const response = await fetch(`/api/people/${personId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password: password })
        });
        
        if (response.ok) {
            loadPeople();
        } else {
            const error = await response.json();
            alert(error.error || 'Chyba při mazání člověka');
        }
    } catch (error) {
        console.error('Chyba:', error);
    }
}

// Bezpečné zobrazení textu (prevence XSS)
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

function getPassword() {
    return prompt('Zadej heslo pro administraci:');
}

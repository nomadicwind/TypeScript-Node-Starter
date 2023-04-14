async function markDocAsRead(event: Event, id: string): Promise<void> {
    // Your markDocAsRead logic
    event.preventDefault();
    const button = event.target as HTMLButtonElement;
    const id2 = button.getAttribute("data-id");

    console.log("id: " + id2);
    type KeyValuePairs = Record<string, boolean>;
    const apiUrl = `/doc/${id2}`;

    const myRecord: KeyValuePairs = {
      "read": true
    };

    const response = await fetch(apiUrl, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(myRecord),
    });
   
 

    // Disable the button and update its style
    button.disabled = true;
    button.classList.add('disabled');
  }
  
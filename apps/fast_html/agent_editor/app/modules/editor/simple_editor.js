/*
notes on exec command deprecation https://stackoverflow.com/questions/60581285/execcommand-is-now-obsolete-whats-the-alternative
*/


function handlePaste(event) {
    /*
    The handle paste is currently just to paste links
    */
    console.log("pasting", event);

    const clipboardData = event.clipboardData || window.clipboardData;
    const pastedData = clipboardData.getData("Text").trim(); // Get the pasted text
    const regex =
        /^(https?:\/\/)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(\/[^\s]*)?$/;

    //the url pasting case
    if (regex.test(pastedData)) {
        event.preventDefault();
        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        const selectedText = selection.toString();
        if (selectedText) {
            //wrapper div needed for clickable links
            const wrapperDiv = document.createElement("span");
            wrapperDiv.className = "editor-links";
            wrapperDiv.contentEditable = "false";

            const aTag = document.createElement("a");
            aTag.href = pastedData;
            aTag.target = "_blank";
            aTag.rel = "noopener noreferrer";
            aTag.textContent = selectedText;
            wrapperDiv.appendChild(aTag);

            range.deleteContents();
            range.insertNode(wrapperDiv);
            selection.removeAllRanges();
        }
    }
}

function replaceSymbolWithSpan(event, editableDiv) {
    /*
    This is a simple scheme to play with HTMX replacing spans of our choosing from a drop down
    */
    if (editableDiv != undefined) {
        console.log('replacing...', editableDiv)
        v = event.key
        event.preventDefault();
        const currentTimestamp = 'id_' + Date.now();
        const span = document.createElement("span");
        span.id = currentTimestamp;
        span.textContent = v;

        const selection = window.getSelection();
        const range = selection.getRangeAt(0);
        range.deleteContents();
        range.insertNode(span);

        range.setStartAfter(span);
        range.setEndAfter(span);
        selection.removeAllRanges();
        selection.addRange(range);

        console.log(event.target)
        console.log(editableDiv.innerHTML);

        console.log("verify insertion");
        console.log(document.getElementById(currentTimestamp));

        return { tid: currentTimestamp, content: editableDiv.innerHTML };
    }
}


function keydown_handler(event) {
    /*
    this keydown handler deals with some key commands - because htmx is used we disabled the first but here
    we can add headings and styled texts and lists as part of a basic editing experience
    image pasting is handled by default
    */
    if (["#", "@", "/"].includes(event.key)) {
        //replaceSymbolWithSpan(event);
    } else {
        const selection = window.getSelection();

        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);
            const selectedText = selection.toString();

            if (event.ctrlKey || event.metaKey) {
                if (
                    ["b", "i", "1", "2", "3", "4", "5", "o", "l"].includes(
                        event.key
                    )
                ) {
                    event.preventDefault();
                }
                switch (event.key) {
                    case "b":
                        document.execCommand("bold");
                        break;
                    case "i":
                        document.execCommand("italic");
                        break;
                    case "1":
                    case "2":
                    case "3":
                    case "4":
                    case "5":
                        const headingLevel = event.key;
                        document.execCommand(
                            "formatBlock",
                            false,
                            `H${headingLevel}`
                        );
                        break;
                    case "o":
                        document.execCommand("insertUnorderedList");
                        break;
                    case "l":
                        document.execCommand("insertOrderedList");
                        break;
                }
            }
        }
    }

} 
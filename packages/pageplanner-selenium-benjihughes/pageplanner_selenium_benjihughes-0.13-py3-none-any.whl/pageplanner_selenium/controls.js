(function(){

    var linkSelector = "#res .srg .rc .r > a";
    var variantsSelector = "#res .rc b, #res .rc strong, #res .rc em";

    var seleniumTriggerId = 'selenium-trigger-56789';

    var linksTableBody = null;
    var linksJsonArea = null;

    var caughtLinks = [];
    var rankedLinks = [];

    function createUIControls(){

        var container = document.createElement("section");
        container.style = "border: 1px solid #dae1e7; border-radius: 8px; background:#f1f5f8; top:0;right:0;position:fixed;z-index: 999999;margin:3rem; padding:2rem; margin-top:6rem; box-shadow: 3px 5px 5px rgba(0,0,0,0.4); max-width: 375px; width: 375px; max-height: 500px; overflow-y: auto;";

        var title = document.createElement('strong');
        title.style = 'display:block; margin-bottom:1rem; font-size:1.2rem';
        title.textContent = 'SERP Selector';
        container.appendChild(title);

        var list = document.createElement('ol');

        var instructions = [
            'Click on a SERP result to add it to your selection',
            'Hit the Analyze button when you\'re done!',
        ];

        for(var i = 0; i< instructions.length; i++){
            var item = document.createElement('li');
            item.textContent = instructions[i];
            item.style = 'list-style: inherit; list-style-position:inside; margin-bottom:0.4rem;';
            list.appendChild(item);
        }
        container.appendChild(list);

        var button = document.createElement("Button");
        button.innerHTML = "Analyze";
        button.style = "margin-top:1rem; margin-bottom:1rem; padding:0.6rem 0.8rem;font-size:1.2rem;min-width:180px; background:#0095ff;box-shadow:inset 0 1px 0 #66bfff;border: 1px solid #07c; color:#fff; cursor: pointer;";
        button.addEventListener('click', addTriggerEl);
        container.appendChild(button);

        // Creating the initial links table structure.
        var linksTable = document.createElement("table");

        var tableHead = document.createElement("thead");
        tableHead.style= "color: #868aa0; text-align: left;";
        var tableHeadRow = document.createElement("tr");
        var tableHeaders = ['Rank', 'Page Link', 'Remove'];
        for(var i = 0; i < tableHeaders.length; i++) {
            var th = document.createElement('th');
            th.style = "padding:3px;";
            th.textContent = tableHeaders[i];
            tableHeadRow.appendChild(th);
        }
        tableHead.appendChild(tableHeadRow);
        linksTable.appendChild(tableHead);

        var tableBody = document.createElement("tbody");
        linksTableBody = tableBody;
        linksTable.appendChild(tableBody);
        container.appendChild(linksTable);

        /* ADDITIONAL COLLAPSIBLE SECTIONS  */

        // Divider
        var hr = document.createElement('hr');
        hr.style = "margin: 1rem 0; border:0; background: #eaeaea; height: 1px";
        container.appendChild(hr);

        var sectionHeader = document.createElement('strong');
        sectionHeader.style="display:block; margin-top: 0.3rem; margin-bottom:0.4rem; font-size:1.1rem;";
        sectionHeader.textContent = 'Extra Tools';
        container.appendChild(sectionHeader);

        var sectionDescription = document.createElement('p');
        sectionDescription.style = "font-size:1rem; color: #595959; margin-bottom:1rem;";
        sectionDescription.textContent = 'These help extract captured data manually.';
        container.appendChild(sectionDescription);

        var linkJsonButton = document.createElement("button");
        linkJsonButton.innerHTML = "See JSON Selection +";
        linkJsonButton.classList.add("ui-control-collapse");
        linkJsonButton.style = "display: block;background: 0;border: 0;font-weight: 700;font-size: 0.9rem;margin: 0.5rem 0;padding: 0;cursor: pointer;";
        var linkJsonCollapse = document.createElement("div");
        linkJsonCollapse.style = "display: none;";
        var linkJsonArea = document.createElement("textarea");
        linkJsonArea.style = "height: 60px; width: 100%; margin: 0.5rem 0; font-size: 1rem;";
        linksJsonArea = linkJsonArea;
        linkJsonCollapse.appendChild(linkJsonArea);
        container.appendChild(linkJsonButton);
        container.appendChild(linkJsonCollapse);


        var variantKwButton = document.createElement("button");
        variantKwButton.innerHTML = "Get Variant Kws +";
        variantKwButton.classList.add("ui-control-collapse");
        variantKwButton.style = "display: block;background: 0;border: 0;font-weight: 700;font-size: 0.9rem;margin: 0.5rem 0;padding: 0;cursor: pointer;";
        var variantKwCollapse = document.createElement("div");
        variantKwCollapse.style = "display: none;";
        var variantKwArea = document.createElement("textarea");
        variantKwArea.style = "height: 60px; width: 100%; margin: 0.5rem 0; font-size: 1rem;";
        var getVariantsButton = document.createElement("button");
        getVariantsButton.style = "margin-bottom:0.4rem; padding:0.2rem 0.4rem;font-size:1rem; background:#0095ff;box-shadow:inset 0 1px 0 #66bfff;border: 1px solid #07c; color:#fff; cursor: pointer;";
        getVariantsButton.innerHTML = 'Extract Variants';
        getVariantsButton.addEventListener('click', function(){
           variantKwArea.value = extractVariants();
        });
        variantKwCollapse.appendChild(variantKwArea);
        variantKwCollapse.appendChild(getVariantsButton);
        container.appendChild(variantKwButton);
        container.appendChild(variantKwCollapse);


        // Add whole UI controls section to page.
        document.body.appendChild(container);
    }

    /**
     * Add the trigger element along with the JSON representation of the selected links.
     */
    function addTriggerEl(){
        var triggerElement = document.createElement('span');
        triggerElement.style = 'display: none;';
        triggerElement.id = seleniumTriggerId;
        triggerElement.textContent = JSON.stringify(caughtLinks);
        document.body.appendChild(triggerElement);
    }

    function init(){
        createUIControls();
        addCollapseListeners();
        rankLinks();
        catchExistingLinks();
    }

    function extractVariants(){
        var words = Array.from(document.querySelectorAll(variantsSelector));
        words = words.map(function(el){
            return el.textContent.trim().toLowerCase();
        });
        // Only unique words
        words = words.filter(function(value, index, self) {
            return self.indexOf(value) === index;
        });
        // Sort by number of words

        words.sort(function(a, b){ return b.split(' ').length - a.split(' ').length } );
        return words.join('\n');
    }

    function addCollapseListeners(){
        var col = document.querySelectorAll(".ui-control-collapse");
        for (var i = 0; i < col.length; i++) {
          col[i].addEventListener("click", function() {
            var content = this.nextElementSibling;
            if (content.style.display === "block") {
              content.style.display = "none";
            } else {
              content.style.display = "block";
            }
          });
        }
    }
    function rankLinks(){
        var links = document.querySelectorAll(linkSelector);
        for(var i = 0; i < links.length; i++) {
            rankedLinks[i+1] = links[i]['href'];
        }
    }

    function findRank(href){
        return rankedLinks.indexOf(href);
    }

    function catchExistingLinks(){
        var links = document.querySelectorAll(linkSelector);
        for(var i = 0; i < links.length; i++){

            // Remove all existing event listeners by recreating the link as a clone.
            var oldLink = links[i];
            var freshLink = oldLink.cloneNode(true);
            oldLink.parentNode.replaceChild(freshLink, oldLink);

            freshLink.addEventListener('click', function(ev){
                ev.preventDefault();
                ev.stopPropagation();
                var href = this['href'];

                // If the link a cloaked Google URL, we can grab the real one from a child node.
                if(href.includes('google.com')){
                    var cite = this.querySelector('cite');
                    href = cite.textContent;
                }
                addLink(href);
            })
        }
    }

    function addLink(href){
        caughtLinks.push({'rank': findRank(href), 'url': href});
        updateLinksUI();
    }

    function removeLink(index){
        caughtLinks.splice(index, 1);
        updateLinksUI();
    }

    function updateLinkRank(index, newValue){
        caughtLinks[index]['rank'] = newValue;
        updateLinksUI();
    }

    function updateLinkHref(index, newValue){
        caughtLinks[index]['url'] = newValue;
        updateLinksUI();
    }

    /**
     * Update the links table with the current contents of caught links.
     */
    function updateLinksUI(){

        linksTableBody.innerHTML = '';
        linksJsonArea.value = JSON.stringify(caughtLinks);

        for(var i = 0; i < caughtLinks.length; i++){

            var currentLink = caughtLinks[i];

            var tr = document.createElement("tr");

            var rankCell = document.createElement("td");
            var rankInput = document.createElement("input");
            rankInput.type = 'text';
            rankInput.style = "width: 30px; padding:3px; border: 1px solid #dae1e7; border-radius: 2px; background:#fbfbfb;";
            rankInput.value = currentLink['rank'];
            rankInput.setAttribute('data-link-index', i.toString());
            rankInput.addEventListener('blur', function(){
                var index = this.getAttribute('data-link-index');
                updateLinkRank(index, this.value);
            });
            rankCell.appendChild(rankInput);
            tr.appendChild(rankCell);


            var hrefCell = document.createElement("td");
            var hrefInput = document.createElement("input");
            hrefInput.type = 'text';
            hrefInput.style = "display:block; width:265px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; padding:3px; border: 1px solid #dae1e7; border-radius: 2px; background:#fbfbfb;";
            hrefInput.title = currentLink['url'];
            hrefInput.value = currentLink['url'];
            hrefInput.setAttribute('data-link-index', i.toString());
            hrefInput.addEventListener('blur', function(){
                var index = this.getAttribute('data-link-index');
                updateLinkHref(index, this.value);
            });
            hrefCell.appendChild(hrefInput);
            tr.appendChild(hrefCell);

            var removeCell = document.createElement("td");
            removeCell.style="text-align: center;";
            var removeButton = document.createElement("button");
            removeButton.textContent = 'X';
            removeButton.style = "background:#dc3545;box-shadow:inset 0 1px 0 #f56e5e; border: 1px solid #a5544a; color:#fff; cursor: pointer; border-radius:2px;";
            removeButton.setAttribute('data-link-index', i.toString());
            removeButton.addEventListener('click', function(){
                var index = this.getAttribute('data-link-index');
                removeLink(index);
            });
            removeCell.appendChild(removeButton);
            tr.appendChild(removeCell);

            linksTableBody.appendChild(tr);
        }
    }

    init();

})();


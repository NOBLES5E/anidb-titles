const {  load } = require("cheerio");
const {writeFileSync, readFileSync } = require("fs");
const animeTitleUrl = "./anime-titles.xml";
const printAllAnimesTitles = async () => {
    const $ = load(readFileSync(animeTitleUrl, "utf-8"));
    const titles = $("animetitles anime").map((_, anime) => {
        const aid = $(anime).attr("aid");
        const titles = $(anime).find("title").map((_, title) => {
            const lang = $(title).attr("xml:lang");
            const type = $(title).attr("type");
            const text = $(title).text();

            return { lang, type, text };
        }).get();

        return { aid, titles };
    }).get();

    writeFileSync("./animes-titles.json", JSON.stringify(titles, null, 2));
}

printAllAnimesTitles();

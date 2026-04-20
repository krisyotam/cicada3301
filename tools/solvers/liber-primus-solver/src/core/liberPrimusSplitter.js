export class LiberPrimusSplitter {

    splittersByName = new Map([
        ['word', '-'],
        ['clause', '.'],
        ['paragraph', '&'],
        ['segment', '$'],
        ['chapter', '§'],
        ['line', '/'],
        ['page', '%'],
    ])

    constructor() {
        if (!!LiberPrimusSplitter.instance) {
            return LiberPrimusSplitter.instance
        }

        LiberPrimusSplitter.instance = this

        return this
    }

    getSplitterChar = splitter => this.splittersByName.get(splitter)

    split = (fileData, splitter) => {
        if (!this.splittersByName.has(splitter))
            throw `unsupported splitter: ${splitter}`

        return fileData.split(this.splittersByName.get(splitter))
    }
}
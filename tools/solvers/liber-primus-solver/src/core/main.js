import {LiberPrimusSolver} from './liberPrimusSolver'

export const main = async () => {
    const solver = new LiberPrimusSolver()
    await solver.run()
}
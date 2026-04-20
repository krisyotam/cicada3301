import {Logger} from '../../utils/logger'
import {phi} from '../../utils/mathUtils'

export class ScanTotientTask {
    constructor() {
        this.logger = new Logger()
    }

    apply = taskConfiguration => {
        const {valuesToSearch} = taskConfiguration

        const valuesToSearchLeft = new Set(valuesToSearch)

        this.logger.log('ScanTotientTask', 'Searching for n values... This may never end, be prepared to manually stop the program')

        for (let n = 1; valuesToSearchLeft.size > 0; n++) {
            const currentValue = phi(n)

            if (valuesToSearchLeft.has(currentValue)) {
                this.logger.log('ScanTotientTask', `Found! phi(${n}) = ${currentValue}`)
                valuesToSearchLeft.delete(currentValue)
                this.logger.log('ScanTotientTask', `Still searching for ${Array.from(valuesToSearchLeft.values())}`)
            }
        }
    }
}
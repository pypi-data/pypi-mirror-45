import { BasicViewerContext } from '../context'
import PropTypes from 'prop-types'
import React from 'react'
import compose from 'recompose/compose'
import { withStyles } from '@material-ui/core/styles'
import withWidth from '@material-ui/core/withWidth'

const styles = theme => ({

})
class MapViewer extends React.Component {
	constructor(props) {
		super(props)
	}
	componentDidMount() {
		const { map } = this.context
		map.setTarget(this.mapDiv)
	}
	componentDidUpdate(prevProps, prevState) {
		const { width } = this.props
		const { map } = this.context

		if (prevProps.width !== width) {
			map.updateSize()
		}
	}
	render() {
		return <div id="map" ref={(mapDiv) => this.mapDiv = mapDiv} className="map-panel"></div>
	}
}
MapViewer.contextType = BasicViewerContext
MapViewer.propTypes = {
	classes: PropTypes.object.isRequired,
	width: PropTypes.any.isRequired,
}
export default compose(withStyles(styles), withWidth())(MapViewer)